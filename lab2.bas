Attribute VB_Name = "NewMacros"
Sub lab2()
    Dim bitString As String
    Dim doc As Document
    Dim i As Long ' ������� ��� �� Long ��� ������ � �������� ��������
    
    ' ������� ���� � ��������� ����������
    Open "/Users/daniilanisimov/Documents/str.txt" For Input As #1
    bitString = Input$(LOF(1), 1) ' ��������� ���������� ����� ��� ������
    Close #1 ' ������� ����
    
    ' ������� ������� �������� Word
    Set doc = ActiveDocument
    
    ' ���������� ������� ������
    For i = 1 To Len(bitString)
        Dim bitChar As String
        bitChar = Mid(bitString, i, 1)
        
        Dim docChar As Range
        Set docChar = doc.Characters(i)
        
        If bitChar = "1" Then
            docChar.HighlightColorIndex = wdWhite
        End If
    Next i
    
    ' ��������� �� �������� ���������� �������
    MsgBox "������ �������� �������."
End Sub

