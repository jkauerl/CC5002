CREATE TABLE comentario (
    id                   int8           auto_increment,
    nombre               varchar(255)   not null,
    email                varchar(255)   not null,
    fecha                datetime       not null,
    comentario           varchar(512)   not null,
    id_donacion          INT            null,
    id_pedido            INT            null,
    primary key(id),
    foreign key(id_donacion) references donacion(id),
    foreign key(id_pedido) references pedido(id)
) 
ENGINE = INNODB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;
