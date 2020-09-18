# add this to the database
# adds a suffix to the citename column in publications if the citename is a dublicate
drop trigger if exists changeCitenameInsert;

delimiter |

CREATE TRIGGER changeCitenameInsert BEFORE INSERT ON publications
  FOR EACH ROW BEGIN
     declare original_slug varchar(255);
     declare slug_counter int;
     set original_slug = new.citename;
     set slug_counter = 1;
     while exists (select true from publications where citename = new.citename) do
        set new.citename = concat(original_slug, '-', slug_counter);
        set slug_counter = slug_counter + 1;
     end while;

  END;
|
delimiter ;


drop trigger if exists changeCitenameUpdate;

delimiter |

CREATE TRIGGER changeCitenameUpdate BEFORE UPDATE ON publications
  FOR EACH ROW BEGIN
     declare original_slug varchar(255);
     declare slug_counter int;
     set original_slug = new.citename;
     set slug_counter = 1;
     while exists (select true from publications where citename = new.citename) do
        set new.citename = concat(original_slug, '-', slug_counter);
        set slug_counter = slug_counter + 1;
     end while;

  END;
|
delimiter ;