alter table etape drop constraint  etape_ordinal_seance_id_key;
alter table etape add unique (seance_id, ordinal) deferrable initially deferred;

alter table seance drop constraint seance_sequence_id_ordinal_key;
alter table seance add unique (sequence_id, ordinal) deferrable initially deferred;

