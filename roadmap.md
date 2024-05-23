Verlauf der mamasjourney App: 

Wir haben zunächst die wichtigsten Funktionen in die mamasjourney App integriert und versucht, sie in VS Code zum Laufen zu bringen. Das war Version 1. 
Anschliessend haben wir die Timeline programmiert. Trotz einiger Startschwierigkeiten konnten wir sie erfolgreich implementieren. Auch das Speichern von Blutwerten, Gewichten, Babynamen und Tagebucheinträgen in CSV-Dateien hat geklappt. Version 2
Wir haben ein User-Login mit YAML-Dateien hinzugefügt, jedoch ohne Passwort-Hashes, was eine Problemquelle darstellt. Version 3
Die nächste Herausforderung besteht darin, die App für den Streamlit-Upload vorzubereiten sowie das User-Login zu verbessern, indem wir Passwort-Hashes verwenden und mehrere Userlogin ermöglichen.
Die App konnten wir Uploaden,aber die Timeline konnten wir nicht hinzufügen. 
Grund: https://github.com/giswqs/streamlit-timeline
Issue: https://github.com/giswqs/streamlit-timeline/issues/8
Darum haben wir eine andere Lösung gesucht und vorerst eine Tabelle mit SSW generiert. 
Neue Ziele: noch Sachen verbessern und optimieren, falls machbar. 
