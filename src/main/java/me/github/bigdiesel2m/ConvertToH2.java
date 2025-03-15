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
		List<String> idlist = Files.readAllLines(Path.of("./objidlist.txt"));
		Set<Integer> objects = new HashSet<>();
		for (String id : idlist)
		{
			objects.add(Integer.parseInt(id));
		}

		// THIS DELETES THE DATABASE IF IT ALREADY EXISTS
		Files.deleteIfExists(Path.of("./object_ids.h2.mv.db"));

		// THIS CONNECTS TO THE DATABASE AND CREATES A TABLE FOR OBJECT IDS IN IT
		try (Connection db = DriverManager.getConnection("jdbc:h2:./object_ids.h2;TRACE_LEVEL_FILE=0"))
		{	
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
		}
	}
}
