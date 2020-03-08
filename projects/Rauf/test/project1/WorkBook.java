package com.spreadsheet;

import java.util.ArrayList;
import java.util.List;

public class WorkBook {
private List<SpreadSheet> workBook;
	
	public WorkBook() {
		this.workBook = new ArrayList<SpreadSheet>();
		this.workBook.add(new SpreadSheet("Sheet_1"));
		this.workBook.add(new SpreadSheet("Sheet_2"));
		this.workBook.add(new SpreadSheet("Sheet_3"));
	}
	
	public boolean add(SpreadSheet spreadSheet) {
		boolean retVal = false;
		for (SpreadSheet sheet : this.workBook ) {
			if(sheet.getSpreadSheetName() == spreadSheet.getSpreadSheetName()) {
				retVal = false;
				//return retVal;
				break;
			}else {
				this.workBook.add(spreadSheet);
				retVal = true;
				//return retVal;
				break;
			}
		}
		return retVal;
	}
	
	public int remove(String sheetName) {

		for (SpreadSheet sheet : this.workBook) {
			if(sheet.getSpreadSheetName() == sheetName) {
				int index = this.workBook.indexOf(sheet);
				this.workBook.remove(sheet);
				return index;
			}
		}
		return -1;
	}
	
	public String remove(int index) {
		
		if(index < this.workBook.size() && index >= 0) {
			if(this.workBook.contains(this.workBook.get(index))) {
				return this.workBook.remove(index).getSpreadSheetName();
			}
		}		
		return null;
	}
	
	//Incompelete Method
	public int move(String from, String to, boolean before) {
		int fromIndex = 0;
		int toIndex = 0;
		for(SpreadSheet sheet : this.workBook) {
			if(sheet.getSpreadSheetName()== from) {
				fromIndex = this.workBook.indexOf(sheet);
				
			}
			else if(sheet.getSpreadSheetName() == to) {
				toIndex = this.workBook.indexOf(sheet);
			}
			
		}
		return -1;
	}
	
	//Incompelete Method
	public String move(int from, int to, boolean before) {
		
		
		return null;
	}
	
	public String moveToEnd(int from) {
		
		if(from < this.workBook.size() && from >= 0) {
			SpreadSheet sheet = this.workBook.remove(from);
			this.workBook.add(sheet);
			return sheet.getSpreadSheetName();
		}	
		return null;
	}
	
	public int moveToEnd(String from) {
		
		for(SpreadSheet sheet : this.workBook) {
			if(sheet.getSpreadSheetName() == from) {
				int index = this.workBook.indexOf(sheet);
				SpreadSheet _sheet = this.workBook.remove(index);
				this.workBook.add(_sheet);
				return index;
			}
		}
		return -1;
	}
	
	public int rename(String currentName, String newName) {
		
		for(SpreadSheet sheet : this.workBook) {
			if(sheet.getSpreadSheetName() == currentName) {
				sheet.setSpreadSheetName(newName);
				return this.workBook.indexOf(sheet);
			}
		}
		
		return -1;
	}
	
	public int index(String sheetName) {
		for(SpreadSheet sheet : this.workBook) {
			if(sheet.getSpreadSheetName() == sheetName) {
				return this.workBook.indexOf(sheet);
			}
		}
		return -1;
	}
	
	public String sheetName(int index) {
		if(index < this.workBook.size() && index >=0) {
			return this.workBook.get(index).getSpreadSheetName();
		}
		return null;
	}
	
	public int length() {
		return this.workBook.size();
	}
	
	public void display() {
		for(SpreadSheet sheet : this.workBook) {
			System.out.println(sheet.getSpreadSheetName());
		}
	}
	public List<SpreadSheet> getWorkBook() {
		return workBook;
	}
	
	@Override
	public String toString() {
		String s = "";
		
		for(SpreadSheet sheet : this.workBook) {
			s+= sheet.getSpreadSheetName()+", ";
		}
		return s;
		
	}
}
