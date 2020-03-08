package oop;

public class Test {

	public static void main(String[] args) {
		
		//Person p = new Person("Aman", 22, "Male", "DrigRoad");
		
		/*
		Student s = new Student("Aman", 22, "Male", "DrigRoad", 33, "7", "BSSE");
		
		Person p1 = new Student("Rauf", 22, "Male", "DrigRoad", 33, "7", "BSSE");
		
		Student st = (Student)p1; //Downcasting
		System.out.println(st.getRegisterationNumber());
		System.out.println(((Student)p1).getRegisterationNumber());
		System.out.println(st.getTimings("12:30"));
		st.abdullah("Abdullah");

		*/
		
		Calculator calc = new Calculator();
		double result = calc.add(1.5, 2.5, 3.5);
		
		System.out.println(result);
		
	}

}
