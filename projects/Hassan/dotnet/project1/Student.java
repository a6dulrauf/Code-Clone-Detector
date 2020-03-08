package oop;

public class Student extends Person {
	
	private int registrationNumber;
	private String semester;
	private String program;
	
	public Student() {
		
	}
	public Student(String name, int age, String gender, String address,
			int registrationNumber, String semester, String program) {
		
		super(name, age, gender, address);
		//super.setName(name);
		//super.setAge(age);
		//super.setGender(gender);
		//super.setAddress(address);
		this.registrationNumber = registrationNumber;
		this.semester = semester;
		this.program = program;
	}

	public int getRegisterationNumber() {
		return registrationNumber;
	}

	public void setRegistrationNumber(int registrationNumber) {
		this.registrationNumber = registrationNumber;
	}

	public String getSemester() {
		return semester;
	}

	public void setSemester(String semester) {
		this.semester = semester;
	}

	public String getProgram() {
		return program;
	}

	public void setProgram(String program) {
		this.program = program;
	}
	
	@Override
	public void abdullah(String name) {
		System.out.println("Faculty");
		System.out.println("Ilyas");
	}
	
	@Override
	public String getTimings(String timings) {
		System.out.println(timings+"AM");
		return timings;
	}
	

}
