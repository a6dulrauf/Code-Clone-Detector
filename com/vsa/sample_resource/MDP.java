package com.mdp;

import com.elements.Grid;
import com.utilities.Constant;

public class MDP {

	private Double successProbability;
	private Double discount;
	private Double livingReward;
	private Grid grid;
	
	public MDP(Grid grid)
	{
		successProbability = 0.8;
		discount = 0.9;
		livingReward = -0.1;
		this.grid = grid;
	}
	
	public void valueIteration()
	{
		Double exceptionCase = (1 - successProbability)/2;
		for(int i = 0; i < grid.getRows(); i++)
			for(int j = 0; j < grid.getColumns(); j++)
			{
				if(grid.getValue(i, j).getType().equals(Constant.CELL_PENALTY))
				{
					grid.getValue(i, j).setValue(-1.0);
					continue;
				}
				
				if(grid.getValue(i, j).getType().equals(Constant.CELL_REWARD))
				{
					grid.getValue(i, j).setValue(1.0);
					continue;
				}
				
				if(grid.getValue(i, j).getType().equals(Constant.CELL_WALL))
				{
					grid.getValue(i, j).setValue(0.0);
					continue;
				}

				
				Double upValue = 0.0, downValue = 0.0, rightValue = 0.0, leftValue = 0.0, maxValue = Double.MIN_VALUE;
				String action = "NO";
				
/*				if(i == 2 && j == 2)
					System.out.println("aaa");*/
				
				////For NORTH ACTION
					//if north available
					if( i + 1 < grid.getRows() && !grid.getValue(i+1, j).getType().equals(Constant.CELL_WALL))
					{
						upValue += successProbability * (livingReward + discount * grid.getValue(i+1, j).getValue());
					}
					else
					{
						upValue += successProbability * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					//if east available
					if( j + 1 < grid.getColumns() && !grid.getValue(i, j+1).getType().equals(Constant.CELL_WALL))
					{
						upValue += exceptionCase * (livingReward + discount * grid.getValue(i, j+1).getValue());
					}
					else
					{
						upValue += exceptionCase * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					
					//if west available
					if( j - 1 >= 0 && !grid.getValue(i, j-1).getType().equals(Constant.CELL_WALL))
					{
						upValue += exceptionCase * (livingReward + discount * grid.getValue(i, j-1).getValue());
					}
					else
					{
						upValue += exceptionCase * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					if(upValue > maxValue)
					{
						maxValue = upValue;
						action = "UP";
					}

				////For EAST ACTION
					//if north available
					if( j + 1 < grid.getColumns() && !grid.getValue(i, j+1).getType().equals(Constant.CELL_WALL))
					{
						rightValue += successProbability * (livingReward + discount * grid.getValue(i, j+1).getValue());
					}
					else
					{
						rightValue += successProbability * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					//if east available
					if( i - 1 >= 0  && !grid.getValue(i-1, j).getType().equals(Constant.CELL_WALL))
					{
						rightValue += exceptionCase * (livingReward + discount * grid.getValue(i-1, j).getValue());
					}
					else
					{
						rightValue += exceptionCase * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					//if west available
					if( i + 1  < grid.getRows() && !grid.getValue(i+1, j).getType().equals(Constant.CELL_WALL))
					{
						rightValue += exceptionCase * (livingReward + discount * grid.getValue(i+1, j).getValue());
					}
					else
					{
						rightValue += exceptionCase * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					if(rightValue > maxValue)
					{
						maxValue = rightValue;
						action = "EAST";
					}
					
				////For WEST ACTION
					//if north available
					if( j - 1 >= 0 && !grid.getValue(i, j-1).getType().equals(Constant.CELL_WALL))
					{
						leftValue += successProbability * (livingReward + discount * grid.getValue(i, j-1).getValue());
					}
					else
					{
						leftValue += successProbability * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					//if east available
					if( i - 1 >= 0  && !grid.getValue(i-1, j).getType().equals(Constant.CELL_WALL))
					{
						leftValue += exceptionCase * (livingReward + discount * grid.getValue(i-1, j).getValue());
					}
					else
					{
						leftValue += exceptionCase * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					//if west available
					if( i + 1  < grid.getRows() && !grid.getValue(i+1, j).getType().equals(Constant.CELL_WALL))
					{
						leftValue += exceptionCase * (livingReward + discount * grid.getValue(i+1, j).getValue());
					}
					else
					{
						leftValue += exceptionCase * (livingReward + discount * grid.getValue(i, j).getValue());
					}	
					
					if(leftValue > maxValue)
					{
						maxValue = leftValue;
						action = "WEST";
					}
					
					
				////For SOUTH ACTION
					//if north available
					if( i - 1 >= 0 && !grid.getValue(i-1, j).getType().equals(Constant.CELL_WALL))
					{
						downValue += successProbability * (livingReward + discount * grid.getValue(i-1, j).getValue());
					}
					else
					{
						downValue += successProbability * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					//if east available
					if( j + 1 < grid.getColumns() && !grid.getValue(i, j+1).getType().equals(Constant.CELL_WALL))
					{
						downValue += exceptionCase * (livingReward + discount * grid.getValue(i, j+1).getValue());
					}
					else
					{
						downValue += exceptionCase * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					//if west available
					if( j - 1 >= 0 && !grid.getValue(i, j-1).getType().equals(Constant.CELL_WALL))
					{
						downValue += exceptionCase * (livingReward + discount * grid.getValue(i, j-1).getValue());
					}
					else
					{
						downValue += exceptionCase * (livingReward + discount * grid.getValue(i, j).getValue());
					}
					
					if(downValue > maxValue)
					{
						maxValue = downValue;
						action = "SOUTH";
					}
					
					if(!action.equalsIgnoreCase("NO"))
						grid.getValue(i, j).setValue(maxValue);
					grid.getValue(i, j).setDirectionValues(upValue, downValue, rightValue, leftValue);
					grid.getValue(i, j).setAction(action);
					
					
			}
	
	}

	public Double getSuccessProbability() {
		return successProbability;
	}

	public void setSuccessProbability(Double successProbability) {
		this.successProbability = successProbability;
	}

	public Double getDiscount() {
		return discount;
	}

	public void setDiscount(Double discount) {
		this.discount = discount;
	}

	public Double getLivingReward() {
		return livingReward;
	}

	public void setLivingReward(Double livingReward) {
		this.livingReward = livingReward;
	}

	public Grid getGrid() {
		return grid;
	}

	public void setGrid(Grid grid) {
		this.grid = grid;
	}
	
	
	
	
}
