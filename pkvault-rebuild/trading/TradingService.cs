using System.Net;
using System.Net.Sockets;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.DependencyInjection;
using PKHeX.Core;
using Serilog;

namespace PKVault.Core;

public record TradeHostPayload(bool LocalTest);
public record TradeConnectPayload(string Address);
public record TradeOfferPayload(string PkmVariantId);
public record TradeReadyPayload(bool Ready);

public record TradePokemonDTO(
    string? VariantId,
    string PeerName,
    string Nickname,
    ushort Species,
    int Level,
    byte Generation,
    EntityContext Context,
    string Extension,
    string PayloadBase64,
    string Fingerprint
);

public record TradeStateDTO(
    string Status,
    bool IsHost,
    bool Connected,
    string ProfileName,
    string? PeerName,
    string? HostAddress,
    int? ListenPort,
    TradePokemonDTO? LocalOffer,
    TradePokemonDTO? RemoteOffer,
    bool LocalReady,
    bool RemoteReady,
    string? ActiveTransactionId,
    string? LastError
);

public record TradeWireMessage(
    string Type,
    string? TransactionId = null,
    string? ProfileName = null,
    TradePokemonDTO? Offer = null,
    bool? Ready = null,
    string? Error = null
);

public record TradeJournal(string TransactionId, DateTime BackupTime, string Role, string State);

public class TradingService(
    IServiceProvider sp,
    ActionService actionService,
    BackupService backupService,
    ISessionService sessionService
)
{
    public const int LocalTestPort = 24801;

    private readonly object stateLock = new();
    private readonly SemaphoreSlim sendLock = new(1, 1);

    private TcpListener? listener;
    private TcpClient? client;
    private StreamReader? reader;
    private StreamWriter? writer;
    private CancellationTokenSource? networkCts;

    private bool isHost;
    private bool connected;
    private string status = "Disconnected";
    private string? peerName;
    private string? hostAddress;
    private int? listenPort;
    private TradePokemonDTO? localOffer;
    private TradePokemonDTO? remoteOffer;
    private bool localReady;
    private bool remoteReady;
    private string? activeTransactionId;
    private string? lastError;
    private bool stageActive;
    private DateTime? pendingBackupTime;

    private int transactionRunning;
    private TaskCompletionSource<bool>? preparedTcs;
    private TaskCompletionSource<bool>? stagedTcs;
    private TaskCompletionSource<bool>? finalizedTcs;
    private TaskCompletionSource<bool>? confirmedTcs;
    private TaskCompletionSource<bool>? restoredTcs;

    private string ProfileName =>
        Environment.GetEnvironmentVariable("PKVAULT_TRADE_PROFILE")
        ?? Path.GetFileName(Directory.GetCurrentDirectory().TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar))
        ?? "PKVault";

    private string JournalPath => Path.Combine(Directory.GetCurrentDirectory(), "pkvault-trade-pending.json");

    public async Task<TradeStateDTO> GetStateAsync()
    {
        await RecoverAbandonedTradeIfNeededAsync();
        lock (stateLock)
            return BuildState();
    }

    public async Task<TradeStateDTO> HostAsync(bool localTest)
    {
        await DisconnectAsync();
        await RecoverAbandonedTradeIfNeededAsync();

        networkCts = new CancellationTokenSource();
        listener = new TcpListener(localTest ? IPAddress.Loopback : IPAddress.Any, localTest ? LocalTestPort : 0);

        try
        {
            listener.Start(1);
        }
        catch (SocketException ex) when (localTest)
        {
            throw new InvalidOperationException($"Local test address localhost:0000 is already in use by another PKVault host ({ex.SocketErrorCode}).", ex);
        }

        var port = ((IPEndPoint)listener.LocalEndpoint).Port;
        lock (stateLock)
        {
            isHost = true;
            status = "Hosting";
            listenPort = port;
            hostAddress = localTest ? "localhost:0000" : $"localhost:{port}";
            lastError = null;
        }

        _ = AcceptClientAsync(listener, networkCts.Token);
        return await GetStateAsync();
    }

    public async Task<TradeStateDTO> ConnectAsync(string address)
    {
        await DisconnectAsync();
        await RecoverAbandonedTradeIfNeededAsync();

        var (host, port) = ParseAddress(address);
        networkCts = new CancellationTokenSource();

        var tcp = new TcpClient();
        lock (stateLock)
        {
            isHost = false;
            status = "Connecting";
            hostAddress = address;
            listenPort = null;
            lastError = null;
        }

        try
        {
            await tcp.ConnectAsync(host, port, networkCts.Token);
            await SetupPeerAsync(tcp, networkCts.Token);
        }
        catch
        {
            tcp.Dispose();
            lock (stateLock)
                status = "Error";
            throw;
        }

        return await GetStateAsync();
    }

    public async Task<TradeStateDTO> SetOfferAsync(string pkmVariantId)
    {
        if (!connected)
            throw new InvalidOperationException("Connect to another PKVault before offering a Pokemon.");
        if (localReady)
            throw new InvalidOperationException("Unready before changing the offered Pokemon.");
        if (Volatile.Read(ref transactionRunning) != 0)
            throw new InvalidOperationException("A trade is already being committed.");

        var offer = await BuildOfferAsync(pkmVariantId);

        lock (stateLock)
        {
            localOffer = offer;
            localReady = false;
            lastError = null;
        }

        await SendAsync(new("offer", Offer: offer));
        return await GetStateAsync();
    }

    public async Task<TradeStateDTO> SetReadyAsync(bool ready)
    {
        if (!connected)
            throw new InvalidOperationException("No active trade connection.");
        if (ready && localOffer == null)
            throw new InvalidOperationException("Choose a Pokemon before readying.");

        if (ready)
            await ValidateLocalOfferAsync();

        lock (stateLock)
        {
            localReady = ready;
            if (!ready)
                status = "Connected";
        }

        await SendAsync(new("ready", Ready: ready));

        if (ready && isHost && remoteReady)
            _ = RunHostTransactionAsync();

        return await GetStateAsync();
    }

    public async Task<TradeStateDTO> DisconnectAsync()
    {
        try
        {
            if (stageActive)
                await RollbackStageAsync();
            else if (pendingBackupTime != null && status != "Completed")
                await RestorePendingBackupAsync();
        }
        catch (Exception ex)
        {
            Log.Error(ex, "Trade rollback during disconnect failed");
        }

        try { networkCts?.Cancel(); } catch { }
        try { listener?.Stop(); } catch { }
        try { client?.Close(); } catch { }

        listener = null;
        client = null;
        reader = null;
        writer = null;
        networkCts?.Dispose();
        networkCts = null;

        lock (stateLock)
        {
            connected = false;
            isHost = false;
            status = "Disconnected";
            peerName = null;
            hostAddress = null;
            listenPort = null;
            localOffer = null;
            remoteOffer = null;
            localReady = false;
            remoteReady = false;
            activeTransactionId = null;
            lastError = null;
        }

        return BuildState();
    }

    private async Task AcceptClientAsync(TcpListener tcpListener, CancellationToken cancellationToken)
    {
        try
        {
            var accepted = await tcpListener.AcceptTcpClientAsync(cancellationToken);
            tcpListener.Stop();
            await SetupPeerAsync(accepted, cancellationToken);
        }
        catch (OperationCanceledException)
        {
        }
        catch (Exception ex)
        {
            SetError($"Trade host failed: {ex.Message}");
        }
    }

    private async Task SetupPeerAsync(TcpClient tcp, CancellationToken cancellationToken)
    {
        client = tcp;
        var stream = tcp.GetStream();
        reader = new StreamReader(stream, new UTF8Encoding(false), false, 8192, leaveOpen: true);
        writer = new StreamWriter(stream, new UTF8Encoding(false), 8192, leaveOpen: true) { AutoFlush = true };

        lock (stateLock)
        {
            connected = true;
            status = "Connected";
            lastError = null;
        }

        await SendAsync(new("hello", ProfileName: ProfileName));
        if (localOffer != null)
            await SendAsync(new("offer", Offer: localOffer));

        _ = ReadLoopAsync(cancellationToken);
    }

    private async Task ReadLoopAsync(CancellationToken cancellationToken)
    {
        try
        {
            while (!cancellationToken.IsCancellationRequested && reader != null)
            {
                var line = await reader.ReadLineAsync(cancellationToken);
                if (line == null)
                    break;

                var msg = JsonSerializer.Deserialize(line, RouteJsonContext.DefaultWithOptions.TradeWireMessage)
                    ?? throw new InvalidDataException("Empty trade protocol message.");

                await HandleWireMessageAsync(msg);
            }
        }
        catch (OperationCanceledException)
        {
        }
        catch (Exception ex)
        {
            SetError($"Trade connection failed: {ex.Message}");
        }
        finally
        {
            if (!cancellationToken.IsCancellationRequested)
            {
                try
                {
                    if (stageActive)
                        await RollbackStageAsync();
                }
                catch (Exception ex)
                {
                    Log.Error(ex, "Trade stage rollback after connection loss failed");
                }

                lock (stateLock)
                {
                    connected = false;
                    if (status != "Completed")
                        status = "Disconnected";
                }
            }
        }
    }

    private async Task HandleWireMessageAsync(TradeWireMessage msg)
    {
        switch (msg.Type)
        {
            case "hello":
                lock (stateLock)
                {
                    peerName = msg.ProfileName ?? "PKVault peer";
                    status = "Connected";
                }
                break;

            case "offer":
                lock (stateLock)
                {
                    remoteOffer = msg.Offer;
                    remoteReady = false;
                }
                break;

            case "ready":
                lock (stateLock)
                    remoteReady = msg.Ready == true;

                if (isHost && localReady && remoteReady)
                    _ = RunHostTransactionAsync();
                break;

            case "prepare":
                if (isHost)
                    break;
                try
                {
                    await ValidateLocalOfferAsync();
                    await SendAsync(new("prepared", TransactionId: msg.TransactionId));
                }
                catch (Exception ex)
                {
                    await SendAsync(new("error", TransactionId: msg.TransactionId, Error: ex.Message));
                }
                break;

            case "prepared":
                preparedTcs?.TrySetResult(true);
                break;

            case "stage":
                if (isHost || msg.Offer == null)
                    break;
                try
                {
                    await StageLocalSwapAsync(msg.TransactionId!, msg.Offer);
                    await SendAsync(new("staged", TransactionId: msg.TransactionId));
                }
                catch (Exception ex)
                {
                    await SendAsync(new("error", TransactionId: msg.TransactionId, Error: ex.Message));
                }
                break;

            case "staged":
                stagedTcs?.TrySetResult(true);
                break;

            case "finalize":
                if (isHost)
                    break;
                try
                {
                    await PersistStagedTradeAsync(msg.TransactionId!, "Participant");
                    await SendAsync(new("finalized", TransactionId: msg.TransactionId));
                }
                catch (Exception ex)
                {
                    await SendAsync(new("error", TransactionId: msg.TransactionId, Error: ex.Message));
                }
                break;

            case "finalized":
                finalizedTcs?.TrySetResult(true);
                break;

            case "confirm":
                if (isHost)
                    break;
                lock (stateLock)
                {
                    status = "Completed";
                    localReady = false;
                    remoteReady = false;
                }
                await SendAsync(new("confirmed", TransactionId: msg.TransactionId));
                await ClearPendingJournalAsync();
                break;

            case "confirmed":
                confirmedTcs?.TrySetResult(true);
                break;

            case "rollback-stage":
                await RollbackStageAsync();
                await SendAsync(new("rolled-back", TransactionId: msg.TransactionId));
                break;

            case "restore-committed":
                await RestorePendingBackupAsync();
                await SendAsync(new("restored", TransactionId: msg.TransactionId));
                break;

            case "restored":
                restoredTcs?.TrySetResult(true);
                break;

            case "error":
                var error = msg.Error ?? "Peer reported an unknown trading error.";
                FailWaiters(error);
                SetError(error);
                break;
        }
    }

    private async Task RunHostTransactionAsync()
    {
        if (Interlocked.Exchange(ref transactionRunning, 1) != 0)
            return;

        var tx = Guid.NewGuid().ToString("N");
        var clientStaged = false;
        var localStaged = false;
        var clientPersisted = false;
        var localPersisted = false;

        try
        {
            TradePokemonDTO hostOffer;
            TradePokemonDTO clientOffer;
            lock (stateLock)
            {
                if (!connected || !localReady || !remoteReady || localOffer == null || remoteOffer == null)
                    return;

                hostOffer = localOffer;
                clientOffer = remoteOffer;
                activeTransactionId = tx;
                status = "Trading";
                lastError = null;
            }

            await ValidateLocalOfferAsync();

            preparedTcs = NewWaiter();
            await SendAsync(new("prepare", TransactionId: tx));
            await preparedTcs.Task.WaitAsync(TimeSpan.FromSeconds(20));

            stagedTcs = NewWaiter();
            await SendAsync(new("stage", TransactionId: tx, Offer: hostOffer));
            await stagedTcs.Task.WaitAsync(TimeSpan.FromSeconds(20));
            clientStaged = true;

            await StageLocalSwapAsync(tx, clientOffer);
            localStaged = true;

            finalizedTcs = NewWaiter();
            await SendAsync(new("finalize", TransactionId: tx));
            await finalizedTcs.Task.WaitAsync(TimeSpan.FromSeconds(30));
            clientPersisted = true;

            await PersistStagedTradeAsync(tx, "Coordinator");
            localPersisted = true;

            confirmedTcs = NewWaiter();
            await SendAsync(new("confirm", TransactionId: tx));
            await confirmedTcs.Task.WaitAsync(TimeSpan.FromSeconds(20));

            await ClearPendingJournalAsync();

            lock (stateLock)
            {
                status = "Completed";
                localReady = false;
                remoteReady = false;
                activeTransactionId = null;
            }
        }
        catch (Exception ex)
        {
            Log.Error(ex, "PKVault trade transaction failed");

            try
            {
                if (localPersisted)
                    await RestorePendingBackupAsync();
                else if (localStaged)
                    await RollbackStageAsync();

                if (clientPersisted)
                {
                    restoredTcs = NewWaiter();
                    await SendAsync(new("restore-committed", TransactionId: tx));
                    await restoredTcs.Task.WaitAsync(TimeSpan.FromSeconds(20));
                }
                else if (clientStaged)
                {
                    await SendAsync(new("rollback-stage", TransactionId: tx));
                }
            }
            catch (Exception rollbackEx)
            {
                Log.Error(rollbackEx, "PKVault trade rollback failed");
            }

            SetError($"Trade failed and was rolled back: {ex.Message}");
        }
        finally
        {
            preparedTcs = stagedTcs = finalizedTcs = confirmedTcs = restoredTcs = null;
            Interlocked.Exchange(ref transactionRunning, 0);
        }
    }

    private async Task<TradePokemonDTO> BuildOfferAsync(string pkmVariantId)
    {
        if (!sessionService.HasEmptyActionList())
            throw new InvalidOperationException("Save or undo current PKVault changes before starting a trade.");

        using var scope = sp.CreateScope();
        var loader = scope.ServiceProvider.GetRequiredService<IPkmVariantLoader>();

        var entity = await loader.GetEntity(pkmVariantId)
            ?? throw new KeyNotFoundException($"Pokemon not found: {pkmVariantId}");
        var dto = await loader.CreateDTO(entity);

        if (!dto.IsMain)
            throw new InvalidOperationException("Only the main variant can be offered for trade.");
        if (!dto.IsEnabled || !dto.CanDelete || dto.IsExternal)
            throw new InvalidOperationException("That Pokemon cannot be traded from PKVault.");

        var group = (await loader.GetEntitiesByBox(entity.BoxId, entity.BoxSlot)).Values;
        foreach (var related in group)
        {
            var relatedDto = await loader.CreateDTO(related);
            if (!relatedDto.CanDelete || relatedDto.IsExternal)
                throw new InvalidOperationException("This Pokemon has a protected/external variant and cannot be traded.");
        }

        var pkm = await loader.GetPKM(entity);
        var bytes = pkm.GetDecryptedDataParty();
        var fingerprint = Convert.ToHexString(SHA256.HashData(bytes));

        return new(
            VariantId: entity.Id,
            PeerName: ProfileName,
            Nickname: pkm.Nickname,
            Species: pkm.Species,
            Level: pkm.CurrentLevel,
            Generation: entity.Generation,
            Context: entity.Context,
            Extension: pkm.Extension,
            PayloadBase64: Convert.ToBase64String(bytes),
            Fingerprint: fingerprint
        );
    }

    private async Task ValidateLocalOfferAsync()
    {
        var offer = localOffer ?? throw new InvalidOperationException("No local Pokemon is offered.");
        if (offer.VariantId == null)
            throw new InvalidOperationException("Local trade offer has no PKVault variant id.");

        var current = await BuildOfferAsync(offer.VariantId);
        if (!current.Fingerprint.Equals(offer.Fingerprint, StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("The offered Pokemon changed after it was selected.");
    }

    private async Task StageLocalSwapAsync(string tx, TradePokemonDTO incoming)
    {
        var offer = localOffer ?? throw new InvalidOperationException("No local trade offer.");
        if (offer.VariantId == null)
            throw new InvalidOperationException("Local trade offer has no variant id.");
        if (!sessionService.HasEmptyActionList())
            throw new InvalidOperationException("PKVault has unsaved actions; trade cannot be staged.");

        await actionService.TradeSwap(new(offer.VariantId, incoming));

        stageActive = true;
        lock (stateLock)
        {
            activeTransactionId = tx;
            status = "Trading";
        }
    }

    private async Task RollbackStageAsync()
    {
        if (!stageActive)
            return;

        await actionService.RemoveDataActionsAndReset(0);
        stageActive = false;

        lock (stateLock)
        {
            if (connected)
                status = "Connected";
            activeTransactionId = null;
            localReady = false;
            remoteReady = false;
        }
    }

    private async Task PersistStagedTradeAsync(string tx, string role)
    {
        if (!stageActive)
            throw new InvalidOperationException("No staged trade exists to persist.");

        var flags = new DataUpdateFlags();
        var backupTime = await backupService.CreateBackup($"backup_before_trade_{tx}", flags);
        pendingBackupTime = backupTime;

        await WriteJournalAsync(new(tx, backupTime, role, "Persisting"));

        try
        {
            using var scope = sp.CreateScope();
            await sessionService.PersistSession(scope);
            await sessionService.StartNewSession(checkInitialActions: false, flags);
            stageActive = false;
            await WriteJournalAsync(new(tx, backupTime, role, "Persisted"));
        }
        catch
        {
            await backupService.RestoreBackup(backupTime, withSafeBackup: false, flags);
            pendingBackupTime = null;
            DeleteJournal();
            stageActive = false;
            throw;
        }
    }

    private async Task RestorePendingBackupAsync()
    {
        var backup = pendingBackupTime;
        if (backup == null && File.Exists(JournalPath))
        {
            var json = await File.ReadAllTextAsync(JournalPath);
            var journal = JsonSerializer.Deserialize(json, RouteJsonContext.DefaultWithOptions.TradeJournal);
            backup = journal?.BackupTime;
        }

        if (backup == null)
            return;

        var flags = new DataUpdateFlags();
        await backupService.RestoreBackup(backup.Value, withSafeBackup: false, flags);
        pendingBackupTime = null;
        stageActive = false;
        DeleteJournal();

        lock (stateLock)
        {
            activeTransactionId = null;
            localReady = false;
            remoteReady = false;
            status = connected ? "Connected" : "Disconnected";
        }
    }

    private async Task RecoverAbandonedTradeIfNeededAsync()
    {
        if (!File.Exists(JournalPath) || pendingBackupTime != null || stageActive)
            return;

        try
        {
            var json = await File.ReadAllTextAsync(JournalPath);
            var journal = JsonSerializer.Deserialize(json, RouteJsonContext.DefaultWithOptions.TradeJournal);
            if (journal == null)
            {
                DeleteJournal();
                return;
            }

            pendingBackupTime = journal.BackupTime;
            await RestorePendingBackupAsync();
            Log.Warning($"Recovered abandoned PKVault trade {journal.TransactionId} from backup.");
        }
        catch (Exception ex)
        {
            SetError($"Pending trade recovery failed: {ex.Message}");
        }
    }

    private async Task ClearPendingJournalAsync()
    {
        pendingBackupTime = null;
        DeleteJournal();
        await Task.CompletedTask;
    }

    private async Task WriteJournalAsync(TradeJournal journal)
    {
        var json = JsonSerializer.Serialize(journal, RouteJsonContext.DefaultWithOptions.TradeJournal);
        await File.WriteAllTextAsync(JournalPath, json);
    }

    private void DeleteJournal()
    {
        try
        {
            if (File.Exists(JournalPath))
                File.Delete(JournalPath);
        }
        catch (Exception ex)
        {
            Log.Warning(ex, "Could not delete PKVault trade journal");
        }
    }

    private async Task SendAsync(TradeWireMessage message)
    {
        var currentWriter = writer ?? throw new InvalidOperationException("Trade peer is not connected.");
        var json = JsonSerializer.Serialize(message, RouteJsonContext.DefaultWithOptions.TradeWireMessage);

        await sendLock.WaitAsync();
        try
        {
            await currentWriter.WriteLineAsync(json);
            await currentWriter.FlushAsync();
        }
        finally
        {
            sendLock.Release();
        }
    }

    private static TaskCompletionSource<bool> NewWaiter() =>
        new(TaskCreationOptions.RunContinuationsAsynchronously);

    private void FailWaiters(string error)
    {
        var ex = new InvalidOperationException(error);
        preparedTcs?.TrySetException(ex);
        stagedTcs?.TrySetException(ex);
        finalizedTcs?.TrySetException(ex);
        confirmedTcs?.TrySetException(ex);
        restoredTcs?.TrySetException(ex);
    }

    private void SetError(string error)
    {
        lock (stateLock)
        {
            lastError = error;
            status = "Error";
            localReady = false;
            remoteReady = false;
        }
        FailWaiters(error);
    }

    private TradeStateDTO BuildState() => new(
        Status: status,
        IsHost: isHost,
        Connected: connected,
        ProfileName: ProfileName,
        PeerName: peerName,
        HostAddress: hostAddress,
        ListenPort: listenPort,
        LocalOffer: localOffer,
        RemoteOffer: remoteOffer,
        LocalReady: localReady,
        RemoteReady: remoteReady,
        ActiveTransactionId: activeTransactionId,
        LastError: lastError
    );

    private static (string Host, int Port) ParseAddress(string raw)
    {
        raw = raw.Trim();
        if (string.IsNullOrWhiteSpace(raw))
            throw new ArgumentException("Trade address is empty.");

        var split = raw.LastIndexOf(':');
        if (split <= 0 || split == raw.Length - 1)
            throw new ArgumentException("Use host:port, for example localhost:0000 or 26.10.20.30:52144.");

        var host = raw[..split].Trim();
        if (!int.TryParse(raw[(split + 1)..], out var port) || port < 0 || port > 65535)
            throw new ArgumentException("Trade port is invalid.");

        if (port == 0)
        {
            if (!host.Equals("localhost", StringComparison.OrdinalIgnoreCase)
                && host != "127.0.0.1"
                && host != "::1")
                throw new ArgumentException("Port 0000 is reserved for PKVault localhost testing.");

            port = LocalTestPort;
        }

        return (host, port);
    }
}
