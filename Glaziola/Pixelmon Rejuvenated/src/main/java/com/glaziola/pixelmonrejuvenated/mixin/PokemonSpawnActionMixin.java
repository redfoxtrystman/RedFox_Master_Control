package com.glaziola.pixelmonrejuvenated.mixin;

import com.cobblemon.mod.common.api.spawning.detail.PokemonSpawnAction;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.glaziola.pixelmonrejuvenated.SpiritOctoberSpawns;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Only Cobblemon wild spawning; not commands, eggs, party releases or evolution. */
@Mixin(value = PokemonSpawnAction.class, remap = false)
public abstract class PokemonSpawnActionMixin {
    @Inject(method = "createEntity()Lcom/cobblemon/mod/common/entity/pokemon/PokemonEntity;",
        at = @At("RETURN"), remap = false)
    private void pixelmonrejuvenated$octoberSpiritConversion(CallbackInfoReturnable<PokemonEntity> cir) {
        PokemonEntity entity = cir.getReturnValue();
        if (entity != null) SpiritOctoberSpawns.tryConvert(entity.getPokemon());
    }
}
