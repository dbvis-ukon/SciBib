/*
 * Copyright (C) 2020 University of Konstanz -  Data Analysis and Visualization Group
 * This file is part of SciBib <https://github.com/dbvis-ukon/SciBib>.
 *
 * SciBib is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SciBib is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SciBib.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * Copyright (C) 2020 University of Konstanz -  Data Analysis and Visualization Group
 * This file is part of SciBib <https://github.com/dbvis-ukon/SciBib>.
 *
 * SciBib is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SciBib is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SciBib.  If not, see <http://www.gnu.org/licenses/>.
 */

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