-- CREATE A TABLE FOR CHATROOMS
CREATE TABLE room (
    label       TEXT,   -- ... the chatroom's name
    motto       TEXT    -- ... the chatroom's description
);

-- INSERT DEFAULT ROOM
INSERT INTO room VALUES ( 'global', 'Hello World!' );