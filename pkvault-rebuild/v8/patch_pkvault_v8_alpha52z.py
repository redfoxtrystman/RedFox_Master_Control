from pathlib import Path
import re, sys
root=Path(sys.argv[1]).resolve()
cs=root/'PKVault.Core/contract/ContractService.cs'
t=cs.read_text(encoding='utf-8')

def line(id,new):
    global t
    pat=rf'^\s*(?:D|SpeciesBounty)\("{re.escape(id)}".*$'
    t2,n=re.subn(pat,new,t,count=1,flags=re.M)
    if n!=1: raise RuntimeError(f'alpha52z contract anchor {id}')
    t=t2

# Small underpaying jobs.
line('easy-catch-8','            D("easy-catch-8", ContractTier.Easy, "Busy Ball", "Catch 8 Pokémon after accepting this contract.", 6_000, ContractMetric.CatchCount, 8, [], R("great-ball", 10), R("potion", 6), R("super-potion", 2), R("repel", 4)),')
line('easy-species-5','            D("easy-species-5", ContractTier.Easy, "Five Different Species", "Catch 5 different species after accepting this contract.", 7_000, ContractMetric.DifferentSpeciesCaught, 5, [], R("ultra-ball", 5), R("great-ball", 5), R("super-potion", 4), R("full-heal", 2)),')

# Hard: long-grind/setup/shiny rewards. No Master Balls for shinies.
line('hard-evolve-10','            D("hard-evolve-10", ContractTier.Hard, "Ten Evolutions", "Evolve 10 Pokémon after accepting this contract.", 50_000, ContractMetric.EvolutionCount, 10, [], R("rare-candy", 8), R("pp-up", 3), R("fire-stone", 1), R("water-stone", 1), R("thunder-stone", 1), R("leaf-stone", 1), R("moon-stone", 1), R("sun-stone", 1), R("dusk-stone", 1), R("dawn-stone", 1), R("shiny-stone", 1), R("ice-stone", 1), R("max-revive", 5)),')
line('hard-shiny-1','            D("hard-shiny-1", ContractTier.Hard, "Shiny Hunt", "Catch 1 shiny Pokémon after accepting this contract.", 55_000, ContractMetric.ShinyCatchCount, 1, [], R("rare-candy", 12), R("luxury-ball", 20), R("pp-up", 5), R("pp-max", 2), R("max-revive", 6), R("full-restore", 10), R("bottle-cap", 2), R("shiny-stone", 2)),')
line('hard-catch-75','            D("hard-catch-75", ContractTier.Hard, "Seventy-Five Catches", "Catch 75 Pokémon after accepting this contract.", 60_000, ContractMetric.CatchCount, 75, [], R("ultra-ball", 50), R("rare-candy", 5), R("full-restore", 10), R("max-repel", 10), R("pp-up", 4), R("max-revive", 5)),')
line('hard-species-30','            D("hard-species-30", ContractTier.Hard, "Thirty Species Hunt", "Catch 30 different species after accepting this contract.", 65_000, ContractMetric.DifferentSpeciesCaught, 30, [], R("rare-candy", 10), R("ultra-ball", 30), R("full-restore", 8), R("pp-up", 4), R("max-repel", 8), R("bottle-cap", 1), R("fire-stone", 1), R("water-stone", 1)),')
line('hard-shiny-2','            D("hard-shiny-2", ContractTier.Hard, "Double Shiny Hunt", "Catch 2 shiny Pokémon after accepting this contract.", 75_000, ContractMetric.ShinyCatchCount, 2, [], R("rare-candy", 20), R("luxury-ball", 30), R("pp-up", 8), R("pp-max", 3), R("max-revive", 10), R("full-restore", 15), R("bottle-cap", 3), R("gold-bottle-cap", 1)),')

# Legendary: limited/specific catches should clearly beat their buy-in.
line('legendary-any','            D("legendary-any", ContractTier.Legendary, "Legendary Acquisition", "Catch any 1 Legendary Pokémon after accepting this contract.", 80_000, ContractMetric.SpeciesSetCatchCount, 1, LegendaryPool, R("ultra-ball", 40), R("rare-candy", 8), R("full-restore", 8), R("max-revive", 5), R("pp-up", 5), R("bottle-cap", 1)),')
for id,species,price,stone in [
('legendary-lugia',249,'95_000',None),('legendary-ho-oh',250,'95_000',None),
('legendary-rayquaza',384,'110_000',None),('legendary-dialga',483,'110_000',None),('legendary-palkia',484,'110_000',None),
('legendary-giratina',487,'125_000','dusk-stone'),('legendary-reshiram',643,'125_000','fire-stone'),('legendary-zekrom',644,'125_000','thunder-stone'),
('legendary-xerneas',716,'135_000','shiny-stone'),('legendary-yveltal',717,'135_000','dusk-stone')]:
    if price=='95_000':
        rewards='R("ultra-ball", 50), R("rare-candy", 10), R("full-restore", 8), R("pp-up", 5), R("max-revive", 5), R("bottle-cap", 1)'
    elif price=='110_000':
        rewards='R("ultra-ball", 50), R("rare-candy", 12), R("full-restore", 10), R("pp-up", 6), R("max-revive", 6), R("bottle-cap", 1)'
    else:
        rewards='R("ultra-ball", 60), R("rare-candy", 15), R("full-restore", 12), R("pp-up", 8), R("max-revive", 8), R("bottle-cap", 2)' + (f', R("{stone}", 2)' if stone else '')
    line(id,f'            SpeciesBounty("{id}", ContractTier.Legendary, {species}, {price}, {rewards}),')

old='''            R("master-ball", 1),
            R("ultra-ball", 20),'''
new='''            R("master-ball", rewardSeed.Contains("apex-creation-crisis", StringComparison.Ordinal) ? 3 : 2),
            R("ultra-ball", 20),'''
if old not in t: raise RuntimeError('alpha52z apex master anchor')
t=t.replace(old,new,1)

old='''            ("gold-bottle-cap", 1, 3), ("ability-capsule", 1, 3), ("big-nugget", 3, 8),
            ("hp-up", 3, 8), ("protein", 3, 8), ("iron", 3, 8),
            ("calcium", 3, 8), ("carbos", 3, 8),'''
new='''            ("gold-bottle-cap", 1, 3), ("ability-capsule", 1, 3), ("big-nugget", 3, 8),
            ("bottle-cap", 3, 8), ("rare-candy", 15, 30), ("pp-max", 2, 5),'''
if old not in t: raise RuntimeError('alpha52z apex pool anchor')
t=t.replace(old,new,1)
cs.write_text(t,encoding='utf-8')

shop=root/'frontend/src/shop/shop-page.tsx'
s=shop.read_text(encoding='utf-8')
old_weekly='Weekly rolls are independent: both slots can roll the same tier. A board can have two Mythicals, two Legendaries, neither, or lower-tier weekly contracts. Abandoning an active contract does not refund its purchase price.'
new_weekly='Weekly rolls are independent from Normal through Mythical. Each weekly slot also has a 2% chance to become an Apex contract costing ₽1.5M–₽2.25M with exact multi-Legendary requirements, at least 2 Master Balls, and a 10–15-line premium reward bundle. Abandoning an active contract does not refund its purchase price.'
already='Weekly rolls are independent from Normal through Mythical. Each weekly slot also has a 2% chance to become an Apex contract costing ₽1.5M–₽2.25M with exact multi-Legendary requirements and a 10–15-line premium reward bundle. Abandoning an active contract does not refund its purchase price.'
if old_weekly in s:
    s=s.replace(old_weekly,new_weekly,1)
elif already in s:
    s=s.replace(already,new_weekly,1)
else:
    raise RuntimeError('alpha52z Apex UI description anchor not found')
shop.write_text(s,encoding='utf-8')

# Guards
c=cs.read_text(encoding='utf-8')
for cid in ('hard-shiny-1','hard-shiny-2'):
    assert 'master-ball' not in next(x for x in c.splitlines() if f'D("{cid}"' in x)
assert 'rewardSeed.Contains("apex-creation-crisis", StringComparison.Ordinal) ? 3 : 2' in c
assert 'R("ultra-ball", 40)' in next(x for x in c.splitlines() if 'legendary-any' in x)
print('PASS alpha52z difficulty-to-reward contract rebalance')
