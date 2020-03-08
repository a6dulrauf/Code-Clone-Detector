package com.spreadsheet;

public class Test {

	public static void main(String[] args) {
		WorkBook workBook= new WorkBook();
		//System.out.println(workBook.add(new SpreadSheet("Sheet_1")));
		
		//System.out.println(workBook.remove("Sheet_4"));
		//System.out.println(workBook.remove(2));
		
		//System.out.println(workBook.move("Sheet_1", "Sheet_3", true));
		System.out.println(workBook.moveToEnd("Sheet_1"));
		//System.out.println(workBook.rename("Sheet_2","MySheet"));
		//System.out.println(workBook.index("Sheet_4"));
		//System.out.println(workBook.sheetName(-1));
		System.out.println();
		System.out.println(workBook);
	}

}
