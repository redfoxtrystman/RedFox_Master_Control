using System;
using System.Collections.Generic;
using BepInEx.Logging;
using UnityEngine;
using UnityEngine.Rendering;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Unity-side consumer of SkyCraft's existing render protocol.
    ///
    /// This is the missing Subnautica equivalent of FalloutCraft's Overlay.cpp + WorldRender.cpp:
    /// - HUD/hand/screens come from the overlay triple buffer;
    /// - block/world meshes come from RenderSection + the Minecraft atlas;
    /// - mobs/particles/player meshes come from RenderScene/RenderAvatar + entity textures.
    /// </summary>
    public sealed class MinecraftRenderBridge : IDisposable
    {
        private readonly ManualLogSource _log;
        private readonly BridgeRuntime _runtime;

        private readonly Dictionary<long, SectionVisual> _sections = new Dictionary<long, SectionVisual>();
        private readonly Dictionary<uint, Texture2D> _entityTextures = new Dictionary<uint, Texture2D>();
        private readonly Dictionary<ulong, Material> _entityMaterials = new Dictionary<ulong, Material>();

        private GameObject _root;
        private GameObject _sceneObject;
        private GameObject _avatarObject;
        private Mesh _sceneMesh;
        private Mesh _avatarMesh;

        private Texture2D _atlas;
        private Texture2D _overlay;
        private Material _atlasOpaque;
        private Material _atlasTransparent;

        private bool _overlayBottomUp;
        private ulong _lastOverlayFrame;
        private bool _loggedOverlay;
        private bool _loggedSection;
        private bool _loggedScene;
        private float _nextVisualHealthLog;
        private bool _disposed;

        private sealed class SectionVisual
        {
            public GameObject Object;
            public Mesh Mesh;
        }

        public MinecraftRenderBridge(ManualLogSource log, BridgeRuntime runtime)
        {
            _log = log ?? throw new ArgumentNullException(nameof(log));
            _runtime = runtime ?? throw new ArgumentNullException(nameof(runtime));

            _root = new GameObject("MinecraftSubnautica.RenderRoot");
            UnityEngine.Object.DontDestroyOnLoad(_root);

            _atlasOpaque = CreateMaterial(false);
            _atlasTransparent = CreateMaterial(true);
        }

        public void Tick()
        {
            if (_disposed)
                return;

            // Keep render-ring latency low without monopolizing Unity's main thread.
            _runtime.DrainRender(HandleRenderMessage, 24L << 20);

            if (_runtime.TryAcquireOverlayFrame(out OverlayFrame frame))
                UploadOverlay(frame);

            if (_runtime.MinecraftConnected && Time.unscaledTime >= _nextVisualHealthLog)
            {
                _nextVisualHealthLog = Time.unscaledTime + 5.0f;
                if (!_loggedOverlay || !_loggedSection)
                {
                    VisualDiagnostics d = _runtime.ReadVisualDiagnostics();
                    _log.LogInfo(
                        $"VISUAL BRIDGE STATUS: overlayFrames={d.OverlayFramesPublished}, " +
                        $"overlayState=0x{d.OverlayState:X}, renderHead={d.RenderHead}, " +
                        $"renderTail={d.RenderTail}, overlaySeen={_loggedOverlay}, sectionSeen={_loggedSection}.");
                }
            }

            if (_avatarObject != null && Player.main != null)
                _avatarObject.transform.position = Player.main.transform.position;
        }

        public void DrawOverlay()
        {
            if (_disposed || _overlay == null || _lastOverlayFrame == 0)
                return;

            int oldDepth = GUI.depth;
            Color oldColor = GUI.color;
            Matrix4x4 oldMatrix = GUI.matrix;

            try
            {
                GUI.depth = -10000;
                GUI.color = Color.white;

                // Minecraft marks the GPU readback as bottom-up. Unity's raw texture data is
                // bottom-origin too, so that case draws directly. Top-down sources are flipped.
                Rect uv = _overlayBottomUp
                    ? new Rect(0f, 0f, 1f, 1f)
                    : new Rect(0f, 1f, 1f, -1f);

                GUI.DrawTextureWithTexCoords(
                    new Rect(0f, 0f, Screen.width, Screen.height),
                    _overlay,
                    uv,
                    true);
            }
            finally
            {
                GUI.depth = oldDepth;
                GUI.color = oldColor;
                GUI.matrix = oldMatrix;
            }
        }

        private void HandleRenderMessage(uint type, byte[] payload)
        {
            switch (type)
            {
                case BridgeProtocol.RenderAtlas:
                    ReceiveAtlas(payload);
                    break;
                case BridgeProtocol.RenderAtlasRegion:
                    ReceiveAtlasRegion(payload);
                    break;
                case BridgeProtocol.RenderSection:
                    ReceiveSection(payload);
                    break;
                case BridgeProtocol.RenderClearAll:
                    ClearWorld();
                    break;
                case BridgeProtocol.RenderTexture:
                    ReceiveEntityTexture(payload);
                    break;
                case BridgeProtocol.RenderScene:
                    ReceiveDynamicMesh(payload, true);
                    break;
                case BridgeProtocol.RenderAvatar:
                    ReceiveDynamicMesh(payload, false);
                    break;
                default:
                    // Lights/solids/dug/ragdoll are valid but do not need to block first visible proof.
                    break;
            }
        }

        private void UploadOverlay(OverlayFrame frame)
        {
            if (frame == null || frame.Pixels == null || frame.Width <= 0 || frame.Height <= 0)
                return;

            if (_overlay == null || _overlay.width != frame.Width || _overlay.height != frame.Height)
            {
                DestroyTexture(ref _overlay);
                _overlay = new Texture2D(frame.Width, frame.Height, TextureFormat.RGBA32, false, false);
                _overlay.wrapMode = TextureWrapMode.Clamp;
                _overlay.filterMode = FilterMode.Point;
                _overlay.name = "Minecraft HUD / Hand";
            }

            _overlay.LoadRawTextureData(frame.Pixels);
            _overlay.Apply(false, false);
            _overlayBottomUp = frame.BottomUp;
            _lastOverlayFrame = frame.FrameId;

            if (!_loggedOverlay)
            {
                _loggedOverlay = true;
                _log.LogInfo(
                    $"RENDER PROOF: Minecraft HUD/hand overlay received " +
                    $"{frame.Width}x{frame.Height}, frame={frame.FrameId}, bottomUp={frame.BottomUp}.");
            }
        }

        private void ReceiveAtlas(byte[] payload)
        {
            if (payload == null || payload.Length < BridgeProtocol.RenderAtlasHeaderBytes)
                return;

            int width = I32(payload, 0);
            int height = I32(payload, 4);
            long bytes = (long)width * height * 4L;

            if (width <= 0 || height <= 0 || width > 8192 || height > 8192
                || bytes > int.MaxValue
                || payload.Length < BridgeProtocol.RenderAtlasHeaderBytes + bytes)
                return;

            DestroyTexture(ref _atlas);
            _atlas = new Texture2D(width, height, TextureFormat.RGBA32, true, false);
            _atlas.name = "Minecraft Block Atlas";
            _atlas.wrapMode = TextureWrapMode.Clamp;
            _atlas.filterMode = FilterMode.Point;

            byte[] pixels = new byte[(int)bytes];
            Buffer.BlockCopy(payload, BridgeProtocol.RenderAtlasHeaderBytes, pixels, 0, pixels.Length);
            _atlas.LoadRawTextureData(pixels);
            _atlas.Apply(true, false);

            _atlasOpaque.mainTexture = _atlas;
            _atlasTransparent.mainTexture = _atlas;

            _log.LogInfo($"RENDER PROOF: Minecraft texture atlas received {width}x{height}.");
        }

        private void ReceiveAtlasRegion(byte[] payload)
        {
            if (_atlas == null || payload == null || payload.Length < BridgeProtocol.RenderAtlasRegionHeaderBytes)
                return;

            int x = I32(payload, 0);
            int yTop = I32(payload, 4);
            int width = I32(payload, 8);
            int height = I32(payload, 12);
            long bytes = (long)width * height * 4L;

            if (x < 0 || yTop < 0 || width <= 0 || height <= 0
                || x + width > _atlas.width || yTop + height > _atlas.height
                || bytes > int.MaxValue
                || payload.Length < BridgeProtocol.RenderAtlasRegionHeaderBytes + bytes)
                return;

            // Incoming rows are top-first. Unity SetPixels32 is bottom-first.
            Color32[] colors = new Color32[width * height];
            int src = BridgeProtocol.RenderAtlasRegionHeaderBytes;
            for (int topRow = 0; topRow < height; topRow++)
            {
                int dstRow = height - 1 - topRow;
                for (int px = 0; px < width; px++)
                {
                    int s = src + (topRow * width + px) * 4;
                    colors[dstRow * width + px] =
                        new Color32(payload[s], payload[s + 1], payload[s + 2], payload[s + 3]);
                }
            }

            int unityY = _atlas.height - yTop - height;
            _atlas.SetPixels32(x, unityY, width, height, colors);
            _atlas.Apply(true, false);
        }

        private void ReceiveSection(byte[] payload)
        {
            if (payload == null || payload.Length < BridgeProtocol.RenderSectionHeaderBytes)
                return;

            int sx = I32(payload, 0);
            int sy = I32(payload, 4);
            int sz = I32(payload, 8);
            int vertexCount = I32(payload, 12);
            vertexCount -= vertexCount % 3;

            long key = SectionKey(sx, sy, sz);
            if (vertexCount <= 0)
            {
                RemoveSection(key);
                return;
            }

            long need = BridgeProtocol.RenderSectionHeaderBytes
                + (long)vertexCount * BridgeProtocol.RenderVertexBytes;
            if (vertexCount > 2_000_000 || need > payload.Length)
                return;

            BuildSection(key, sx, sy, sz, payload, BridgeProtocol.RenderSectionHeaderBytes, vertexCount);

            if (!_loggedSection)
            {
                _loggedSection = true;
                _log.LogInfo(
                    $"RENDER PROOF: first Minecraft section rendered at ({sx},{sy},{sz}), " +
                    $"{vertexCount / 3} triangles.");
            }
        }

        private void BuildSection(long key, int sx, int sy, int sz, byte[] payload, int offset, int count)
        {
            RemoveSection(key);

            Vector3[] vertices = new Vector3[count];
            Vector2[] uv = new Vector2[count];
            Color32[] colors = new Color32[count];
            List<int> opaque = new List<int>(count);
            List<int> translucent = new List<int>();

            for (int i = 0; i < count; i++)
            {
                int at = offset + i * BridgeProtocol.RenderVertexBytes;
                vertices[i] = new Vector3(F32(payload, at), F32(payload, at + 4), F32(payload, at + 8));
                uv[i] = new Vector2(F32(payload, at + 12), 1f - F32(payload, at + 16));
                colors[i] = DecodeColor(U32(payload, at + 20));
            }

            for (int t = 0; t < count; t += 3)
            {
                uint flags = U32(payload, offset + t * BridgeProtocol.RenderVertexBytes + 28);
                List<int> target = (flags & 2u) != 0u ? translucent : opaque;
                target.Add(t);
                target.Add(t + 1);
                target.Add(t + 2);
            }

            Mesh mesh = new Mesh();
            mesh.name = $"Minecraft Section {sx},{sy},{sz}";
            if (count > 65535)
                mesh.indexFormat = IndexFormat.UInt32;
            mesh.vertices = vertices;
            mesh.uv = uv;
            mesh.colors32 = colors;
            mesh.subMeshCount = 2;
            mesh.SetTriangles(opaque.ToArray(), 0, true);
            mesh.SetTriangles(translucent.ToArray(), 1, true);
            mesh.RecalculateBounds();

            GameObject obj = new GameObject(mesh.name);
            obj.transform.SetParent(_root.transform, false);
            obj.transform.position = new Vector3(sx * 16f, sy * 16f, sz * 16f);

            MeshFilter filter = obj.AddComponent<MeshFilter>();
            filter.sharedMesh = mesh;

            MeshRenderer renderer = obj.AddComponent<MeshRenderer>();
            renderer.sharedMaterials = new[] { _atlasOpaque, _atlasTransparent };
            renderer.shadowCastingMode = ShadowCastingMode.On;
            renderer.receiveShadows = true;

            _sections[key] = new SectionVisual { Object = obj, Mesh = mesh };
        }

        private void ReceiveEntityTexture(byte[] payload)
        {
            if (payload == null || payload.Length < BridgeProtocol.RenderTextureHeaderBytes)
                return;

            uint id = U32(payload, 0);
            int width = I32(payload, 4);
            int height = I32(payload, 8);
            long bytes = (long)width * height * 4L;

            if (id == 0 || width <= 0 || height <= 0 || width > 4096 || height > 4096
                || bytes > int.MaxValue
                || payload.Length < BridgeProtocol.RenderTextureHeaderBytes + bytes)
                return;

            if (_entityTextures.TryGetValue(id, out Texture2D old))
                UnityEngine.Object.Destroy(old);

            Texture2D texture = new Texture2D(width, height, TextureFormat.RGBA32, false, false);
            texture.name = $"Minecraft Entity Texture {id}";
            texture.wrapMode = TextureWrapMode.Clamp;
            texture.filterMode = FilterMode.Point;

            byte[] pixels = new byte[(int)bytes];
            Buffer.BlockCopy(payload, BridgeProtocol.RenderTextureHeaderBytes, pixels, 0, pixels.Length);
            texture.LoadRawTextureData(pixels);
            texture.Apply(false, false);
            _entityTextures[id] = texture;

            foreach (var pair in _entityMaterials)
            {
                uint materialTexture = (uint)(pair.Key >> 1);
                if (materialTexture == id)
                    pair.Value.mainTexture = texture;
            }
        }

        private void ReceiveDynamicMesh(byte[] payload, bool hasOrigin)
        {
            int header = hasOrigin ? BridgeProtocol.RenderSceneHeaderBytes : BridgeProtocol.RenderAvatarHeaderBytes;
            if (payload == null || payload.Length < header)
                return;

            double ox = 0, oy = 0, oz = 0;
            uint batchCount;
            uint vertexCount;

            if (hasOrigin)
            {
                ox = F64(payload, 0);
                oy = F64(payload, 8);
                oz = F64(payload, 16);
                batchCount = U32(payload, 24);
                vertexCount = U32(payload, 28);
            }
            else
            {
                batchCount = U32(payload, 0);
                vertexCount = U32(payload, 4);
            }

            if (batchCount == 0 || vertexCount == 0)
            {
                ClearDynamicMesh(hasOrigin);
                return;
            }

            long verticesOffset = header + (long)batchCount * BridgeProtocol.RenderBatchBytes;
            long need = verticesOffset + (long)vertexCount * BridgeProtocol.RenderVertexBytes;
            if (batchCount > 4096 || vertexCount > 2_000_000 || need > payload.Length)
                return;

            Vector3[] vertices = new Vector3[vertexCount];
            Vector2[] uv = new Vector2[vertexCount];
            Color32[] colors = new Color32[vertexCount];

            for (int i = 0; i < vertexCount; i++)
            {
                int at = (int)verticesOffset + i * BridgeProtocol.RenderVertexBytes;
                vertices[i] = new Vector3(F32(payload, at), F32(payload, at + 4), F32(payload, at + 8));
                uv[i] = new Vector2(F32(payload, at + 12), 1f - F32(payload, at + 16));
                colors[i] = DecodeColor(U32(payload, at + 20));
            }

            Mesh mesh = hasOrigin ? _sceneMesh : _avatarMesh;
            GameObject obj = hasOrigin ? _sceneObject : _avatarObject;

            if (mesh == null)
            {
                mesh = new Mesh();
                mesh.name = hasOrigin ? "Minecraft Entities / Particles" : "Minecraft Player";
                obj = new GameObject(mesh.name);
                obj.transform.SetParent(_root.transform, false);
                obj.AddComponent<MeshFilter>().sharedMesh = mesh;
                obj.AddComponent<MeshRenderer>();

                if (hasOrigin)
                {
                    _sceneMesh = mesh;
                    _sceneObject = obj;
                }
                else
                {
                    _avatarMesh = mesh;
                    _avatarObject = obj;
                }
            }
            else
            {
                mesh.Clear();
            }

            if (vertexCount > 65535)
                mesh.indexFormat = IndexFormat.UInt32;
            mesh.vertices = vertices;
            mesh.uv = uv;
            mesh.colors32 = colors;
            mesh.subMeshCount = (int)batchCount;

            Material[] materials = new Material[batchCount];
            for (int b = 0; b < batchCount; b++)
            {
                int bat = header + b * BridgeProtocol.RenderBatchBytes;
                uint texture = U32(payload, bat);
                uint first = U32(payload, bat + 4);
                uint count = U32(payload, bat + 8);
                uint flags = U32(payload, bat + 12);

                if (first + count > vertexCount)
                    count = 0;

                int[] indices = new int[count];
                for (int i = 0; i < count; i++)
                    indices[i] = (int)first + i;

                mesh.SetTriangles(indices, b, false);
                materials[b] = MaterialFor(texture, (flags & 1u) != 0u);
            }

            mesh.RecalculateBounds();
            obj.GetComponent<MeshRenderer>().sharedMaterials = materials;
            obj.transform.position = hasOrigin
                ? new Vector3((float)ox, (float)oy, (float)oz)
                : (Player.main != null ? Player.main.transform.position : Vector3.zero);

            if (hasOrigin && !_loggedScene)
            {
                _loggedScene = true;
                _log.LogInfo(
                    $"RENDER PROOF: Minecraft entities/particles mesh received, " +
                    $"{vertexCount / 3} triangles in {batchCount} batches.");
            }
        }

        private Material MaterialFor(uint textureId, bool transparent)
        {
            if (textureId == 0)
                return transparent ? _atlasTransparent : _atlasOpaque;

            ulong key = ((ulong)textureId << 1) | (transparent ? 1UL : 0UL);
            if (_entityMaterials.TryGetValue(key, out Material existing))
                return existing;

            Material material = CreateMaterial(transparent);
            if (_entityTextures.TryGetValue(textureId, out Texture2D texture))
                material.mainTexture = texture;

            _entityMaterials[key] = material;
            return material;
        }

        private static Material CreateMaterial(bool transparent)
        {
            Shader shader = Shader.Find(transparent ? "Unlit/Transparent" : "Unlit/Transparent Cutout");
            if (shader == null)
                shader = Shader.Find("Unlit/Texture");
            if (shader == null)
                shader = Shader.Find("Standard");

            Material material = new Material(shader);
            material.name = transparent ? "Minecraft Transparent" : "Minecraft Opaque";
            if (material.HasProperty("_Cutoff"))
                material.SetFloat("_Cutoff", 0.1f);
            return material;
        }

        private void ClearWorld()
        {
            foreach (SectionVisual section in _sections.Values)
            {
                if (section.Object != null)
                    UnityEngine.Object.Destroy(section.Object);
                if (section.Mesh != null)
                    UnityEngine.Object.Destroy(section.Mesh);
            }
            _sections.Clear();
            ClearDynamicMesh(true);
            ClearDynamicMesh(false);
            _log.LogInfo("Minecraft render world cleared.");
        }

        private void ClearDynamicMesh(bool scene)
        {
            Mesh mesh = scene ? _sceneMesh : _avatarMesh;
            if (mesh != null)
                mesh.Clear();
        }

        private void RemoveSection(long key)
        {
            if (!_sections.TryGetValue(key, out SectionVisual section))
                return;

            _sections.Remove(key);
            if (section.Object != null)
                UnityEngine.Object.Destroy(section.Object);
            if (section.Mesh != null)
                UnityEngine.Object.Destroy(section.Mesh);
        }

        private static long SectionKey(int x, int y, int z)
        {
            unchecked
            {
                long h = x;
                h = h * 73856093L ^ y * 19349663L;
                h = h * 83492791L ^ z * 2971215073L;
                return h;
            }
        }

        private static uint U32(byte[] b, int o) => BitConverter.ToUInt32(b, o);
        private static int I32(byte[] b, int o) => BitConverter.ToInt32(b, o);
        private static float F32(byte[] b, int o) => BitConverter.ToSingle(b, o);
        private static double F64(byte[] b, int o) => BitConverter.ToDouble(b, o);

        private static Color32 DecodeColor(uint rgba)
        {
            return new Color32(
                (byte)(rgba & 0xFF),
                (byte)((rgba >> 8) & 0xFF),
                (byte)((rgba >> 16) & 0xFF),
                (byte)((rgba >> 24) & 0xFF));
        }

        private static void DestroyTexture(ref Texture2D texture)
        {
            if (texture != null)
                UnityEngine.Object.Destroy(texture);
            texture = null;
        }

        public void Dispose()
        {
            if (_disposed)
                return;
            _disposed = true;

            ClearWorld();

            DestroyTexture(ref _atlas);
            DestroyTexture(ref _overlay);

            foreach (Texture2D texture in _entityTextures.Values)
                if (texture != null)
                    UnityEngine.Object.Destroy(texture);
            _entityTextures.Clear();

            foreach (Material material in _entityMaterials.Values)
                if (material != null)
                    UnityEngine.Object.Destroy(material);
            _entityMaterials.Clear();

            if (_atlasOpaque != null)
                UnityEngine.Object.Destroy(_atlasOpaque);
            if (_atlasTransparent != null)
                UnityEngine.Object.Destroy(_atlasTransparent);

            if (_root != null)
                UnityEngine.Object.Destroy(_root);
            _root = null;
        }
    }
}
