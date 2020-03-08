package com.task;

import java.util.Scanner;

public class Test {
	
	//1
	public static void checkNumberRange(int []A, int startingRange, int endRange){
		int inRange = 0;
		int outRange = 0;
		
		for(int i=0; i < A.length; i++){
			
			if(A[i] >= startingRange && A[i] <= endRange){
				inRange++;
				
			}else{
				outRange++;
			}
			
		}
		
		System.out.println("Total numbers of which are out of range : "+outRange);
		System.out.println("Total numbers of which are in range : "+inRange);
		System.out.println("Percentage of out of range: "+((double)outRange/A.length)*100+"%");
	}
	
	
	//2
	public static void studentMarking(int []marks){
		
		int dist = 0, merit = 0,pass = 0, fail = 0;
		
		for(int i = 0; i < marks.length; i++){
			
			if(marks[i] <= 59 && marks[i] >= 50){
				pass++;
			}else if(marks[i] <= 69 && marks[i] >= 60){
				merit++;
			}else if(marks[i]>69 && marks[i] <= 100){
				dist++;
			}else{
				fail++;
			}
		}
		System.out.println("Number of DISTINCTION grades : " + dist);
		System.out.println("Number of PASS grades : " + pass);
		System.out.println("Number of MERIT grades : " + merit);
		System.out.println("Number of FAIL grades : " + fail);
		
		
	}
	
	//3
	public static void counter(){
		Scanner input = new Scanner(System.in);
		int total1 = 0;
		int total2 = 0;
		int counter = 1;
		
		while(counter < 8){
			counter += 1;
			System.out.println("Enter the number : ");
			int number = input.nextInt();
			if (number > 0){
				total1 += number;
			}
			if(number < 0){
				total2 += number;
			}
		}
		System.out.println("Total 1 : " + total1 );
		System.out.println("Total 2 : " + total2);
		
	}
	
	// 3(a) Total 1 : 13 ; Total 2 : -8
	// 3(b)
	public static void total(){
		
		Scanner input = new Scanner(System.in);
		int number = 0;
		System.out.println("Enter -1 to terminate. ");
		int total = 0;
		while (number != -1){
		
			number = input.nextInt();
			if(number != -1){
				total += number;
			}	
		}
		System.out.println("Total except rogue value : "+total);
		
	}
	
	public static int[] takeInput(int noOfInputs){
		
		Scanner input = new Scanner(System.in);
		int A[] = new int[noOfInputs];
		
		for(int i = 0; i < noOfInputs ; i++){
			A[i] = input.nextInt();
		}
		
		return A;
	}
	
	//4
	public static void compare(){
		
		Scanner input = new Scanner(System.in);
		System.out.println("Enter the value of A : ");
		int A = input.nextInt();
		System.out.println("Enter the value of B : ");
		int B = input.nextInt();
		if(A > B){
			int T = A;
			A = B;
			B = T;
		}
		System.out.println("Output values of A = "+ A + " and B = " + B);
	}
	
	// 4(a) A = 38 ; B = 41
	// 4(b) T is used as a temporary container for storing value to perform swaping between A and B
	
	public static void main(String args[]){
		
		//pass the length of the input you want e.g 5
		System.out.println("Enter numbers to check the range : ");
		int A[] = takeInput(5);//{1,2,3333,100000};
		checkNumberRange(A, 1000, 9999);
		
		System.out.println();
		System.out.println("Enter marks : ");
		//pass the length of the input you want e.g 5
		int marks[] = takeInput(5);
		studentMarking(marks)
		;
		System.out.println();
		counter();
		
		System.out.println();
		total();
		
		System.out.println();
		compare();
	}

}
