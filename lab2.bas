Attribute VB_Name = "NewMacros"
Sub lab2()
    Dim bitString As String
    Dim doc As Document
    Dim i As Long ' Изменим тип на Long для работы с большими строками
    
    ' Открыть файл и прочитать содержимое
    Open "/Users/daniilanisimov/Documents/str.txt" For Input As #1
    bitString = Input$(LOF(1), 1) ' Прочитать содержимое файла как строку
    Close #1 ' Закрыть файл
    
    ' Открыть текущий документ Word
    Set doc = ActiveDocument
    
    ' Обработать битовую строку
    For i = 1 To Len(bitString)
        Dim bitChar As String
        bitChar = Mid(bitString, i, 1)
        
        Dim docChar As Range
        Set docChar = doc.Characters(i)
        
        If bitChar = "1" Then
            docChar.HighlightColorIndex = wdWhite
        End If
    Next i
    
    ' Сообщение об успешном выполнении макроса
    MsgBox "Макрос выполнен успешно."
End Sub

