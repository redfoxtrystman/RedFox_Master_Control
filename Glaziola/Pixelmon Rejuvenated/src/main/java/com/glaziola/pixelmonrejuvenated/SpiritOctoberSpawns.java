package com.glaziola.pixelmonrejuvenated;

import com.cobblemon.mod.common.api.pokemon.feature.FlagSpeciesFeature;
import com.cobblemon.mod.common.api.pokemon.feature.SpeciesFeature;
import com.cobblemon.mod.common.pokemon.Pokemon;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.DateTimeException;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Locale;
import java.util.Properties;
import java.util.Set;
import java.util.concurrent.ThreadLocalRandom;

/**
 * October-only chance to turn a *normal* wild Eevee-family spawn into a Spirit
 * without changing native Cobblemon spawn buckets, weights, or level selection.
 * Called only from PokemonSpawnAction#createEntity, i.e. Cobblemon spawner results.
 */
public final class SpiritOctoberSpawns {
    private static final Set<String> EEVEE_FAMILY = Set.of(
        "eevee", "vaporeon", "jolteon", "flareon", "espeon", "umbreon",
        "leafeon", "glaceon", "sylveon");
    private static final Path CONFIG = Path.of("config", "pixelmonrejuvenated", "october-spirit.properties");
    private static volatile boolean enabled = true;
    private static volatile double chancePercent = 0.25; // 1 in 400 ordinary spawns
    private static volatile ZoneId calendarZone = ZoneId.systemDefault();
    private static volatile boolean initialized;

    private SpiritOctoberSpawns() {}

    public static synchronized void initialize() {
        if (initialized) return;
        try {
            Files.createDirectories(CONFIG.getParent());
            if (!Files.exists(CONFIG)) {
                Properties defaults = new Properties();
                defaults.setProperty("enabled", "true");
                defaults.setProperty("chance_percent", "0.25");
                defaults.setProperty("timezone", "SYSTEM");
                try (OutputStream out = Files.newOutputStream(CONFIG)) {
                    defaults.store(out, "October-only Spirit replacement of natural Eevee and Eeveelution spawns. "
                        + "chance_percent is 0 to 100. timezone = SYSTEM or Java ZoneId (e.g. UTC, America/Los_Angeles). "
                        + "Restart the game/server after editing.");
                }
            }
            Properties properties = new Properties();
            try (InputStream in = Files.newInputStream(CONFIG)) {
                properties.load(in);
            }
            enabled = Boolean.parseBoolean(properties.getProperty("enabled", "true").trim());
            double requested = Double.parseDouble(properties.getProperty("chance_percent", "0.25").trim());
            if (!Double.isFinite(requested) || requested < 0 || requested > 100) {
                throw new IllegalArgumentException("chance_percent must be between 0 and 100");
            }
            chancePercent = requested;
            String timezone = properties.getProperty("timezone", "SYSTEM").trim();
            calendarZone = timezone.equalsIgnoreCase("SYSTEM") ? ZoneId.systemDefault() : ZoneId.of(timezone);
        } catch (IOException | IllegalArgumentException | DateTimeException ex) {
            System.err.println("[Pixelmon Rejuvenated] October Spirit spawn config invalid/unreadable; using safe defaults: " + ex);
            enabled = true;
            chancePercent = 0.25;
            calendarZone = ZoneId.systemDefault();
        }
        initialized = true;
    }

    public static void tryConvert(Pokemon pokemon) {
        if (pokemon == null) return;
        if (!initialized) initialize();
        if (!enabled || chancePercent <= 0.0) return;
        if (LocalDate.now(calendarZone).getMonthValue() != 10) return;
        if (pokemon.getSpecies() == null || !EEVEE_FAMILY.contains(pokemon.getSpecies().getName().toLowerCase(Locale.ROOT))) return;
        // Only regular wild Pokemon; never replace Shiny or any existing special appearance.
        if (pokemon.getShiny()) return;
        if (pokemon.getAspects() != null) {
            for (String aspect : pokemon.getAspects()) {
                if (SpecialPaletteKeys.isSpecial(aspect)) return;
            }
        }
        if (pokemon.getForcedAspects() != null) {
            for (String aspect : pokemon.getForcedAspects()) {
                if (SpecialPaletteKeys.isSpecial(aspect)) return;
            }
        }
        if (pokemon.getFeatures() != null) {
            for (SpeciesFeature feature : pokemon.getFeatures()) {
                if (feature instanceof FlagSpeciesFeature flag && flag.getEnabled()
                    && SpecialPaletteKeys.isSpecial(flag.getName())) return;
            }
        }
        if (ThreadLocalRandom.current().nextDouble(100.0) >= chancePercent) return;
        // The registered Cobblemon Spirit feature automatically updates aspects,
        // selects the Ghost-secondary Spirit form, and syncs to clients.
        new FlagSpeciesFeature("spirit", true).apply(pokemon);
    }
}
