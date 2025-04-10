package me.github.bigdiesel2m;

import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Set;
import java.util.HashSet;
import java.util.List;
import java.sql.Statement;
import java.sql.PreparedStatement;
import java.nio.file.Files;
import java.nio.file.Path;

public class ConvertToH2
{
	public static void main(String[] args) throws Exception
	{
		// THIS LOADS THE OBJECT IDS INTO A SET OF INTEGERS
		List<String> obj_ids = Files.readAllLines(Path.of("./obj_ids.txt"));
		Set<Integer> objects = new HashSet<>();
		for (String id : obj_ids)
		{
			objects.add(Integer.parseInt(id));
		}

		// THIS LOADS THE NPC IDS INTO A SET OF INTEGERS
		List<String> npc_ids = Files.readAllLines(Path.of("./npc_ids.txt"));
		Set<Integer> npcs = new HashSet<>();
		for (String id : npc_ids)
		{
			npcs.add(Integer.parseInt(id));
		}

		// THIS DELETES THE DATABASE IF IT ALREADY EXISTS
		Files.deleteIfExists(Path.of("./page_ids.h2.mv.db"));

		// THIS CONNECTS TO THE DATABASE
		try (Connection db = DriverManager.getConnection("jdbc:h2:./page_ids.h2;TRACE_LEVEL_FILE=0"))
		{
			// THIS CREATES A TABLE FOR OBJECT IDS IN IT
			try (Statement stmt = db.createStatement())
			{
				stmt.executeUpdate("CREATE TABLE OBJECTS (ID INTEGER NOT NULL PRIMARY KEY);");
			}

			// THIS TAKES THE SET OF OBJECT IDS AND PUTS THEM INTO THE OBJECTS TABLE IN THE DATABASE
			try (PreparedStatement stmt = db.prepareStatement("INSERT INTO OBJECTS (ID) VALUES (?);"))
			{
				for (Integer id : objects)
				{
					stmt.setInt(1, id);
					stmt.addBatch();
				}

				stmt.executeBatch();
			}

			// THEN WE DO THE SAME FOR NPCS
			try (Statement stmt = db.createStatement())
			{
				stmt.executeUpdate("CREATE TABLE NPCS (ID INTEGER NOT NULL PRIMARY KEY);");
			}

			try (PreparedStatement stmt = db.prepareStatement("INSERT INTO NPCS (ID) VALUES (?);"))
			{
				for (Integer id : npcs)
				{
					stmt.setInt(1, id);
					stmt.addBatch();
				}

				stmt.executeBatch();
			}
		}
	}
}
