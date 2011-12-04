alter table etape add column new_consignes varchar[];
update etape set new_consignes = ARRAY[consignes_criteres];
alter table etape drop column consignes_criteres;
alter table etape rename column new_consignes to consignes_criteres;
