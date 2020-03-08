package hellofx;
import java.util.Random;

import com.displayElements.CheckBoxValue;
import com.displayElements.EmptyCell;
import com.displayElements.PenaltyCell;
import com.displayElements.PlayerCell;
import com.displayElements.RewardCell;
import com.displayElements.WallCell;
import com.elements.Grid;
import com.elements.Value;
import com.mdp.MDP;
import com.utilities.Constant;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.Label;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class Main extends Application {

	private Grid grid;
	private MDP mdp;

	private Integer player_row;
	private Integer player_col;
	private Random random;
	private GridPane pane;
	private Integer[] row_column_Additions;
	private Double[] decisionProbabilites;

	private Text currX;
	private Text currY;
	private Text nextX;
	private Text nextY;
	private Text randomTxt;
	private Text actionTxt;
	private ChoiceBox<CheckBoxValue> cb;

	public Main() {
		grid = new Grid("grid.txt");
		random = new Random(23);
		mdp = new MDP(grid);
	}

	@Override
	public void start(Stage primaryStage) throws Exception {
		pane = new GridPane();
		pane.setHgap(4.0);
		pane.setVgap(4.0);
		HBox root = new HBox(pane);

		Scene scene = new Scene(root);

		initializeElements();
		attachEvents(scene);
		setUpGrid(pane);
		root.getChildren().add(setUpInfoElements());

		primaryStage.setScene(scene);
		primaryStage.show();
	}

	private void initializeElements() {
		currX = new Text();
		currY = new Text();
		nextX = new Text();
		nextY = new Text();
		randomTxt = new Text();
		actionTxt = new Text();
		cb = new ChoiceBox<>(FXCollections.observableArrayList(new CheckBoxValue("Game", 0),
				new CheckBoxValue("Values", 1), new CheckBoxValue("Q-Values", 2)));
		cb.getSelectionModel().selectFirst();

		row_column_Additions = new Integer[6];
		decisionProbabilites = new Double[3];
		decisionProbabilites[0] = mdp.getSuccessProbability();
		decisionProbabilites[1] = mdp.getSuccessProbability() + 0.1;
		decisionProbabilites[2] = 1.0;
	}

	private VBox setUpInfoElements() {

		VBox root = new VBox();

		Label curLabel = new Label("Current Position");
		curLabel.setFont(Font.font(20));

		VBox currPos = new VBox();
		currPos.getChildren().add(curLabel);
		currPos.getChildren().add(new HBox(new Label("Row      :  "), currX));
		currPos.getChildren().add(new HBox(new Label("Column :  "), currY));

		Label curPos = new Label("Current Action");
		curPos.setFont(Font.font(20));

		VBox action = new VBox();
		action.getChildren().add(curPos);
		action.getChildren().add(new HBox(new Label("Action :  "), actionTxt));

		Label curRnd = new Label("Rnd # gen");
		curRnd.setFont(Font.font(20));

		VBox randomNumberBox = new VBox();
		randomNumberBox.getChildren().add(curRnd);
		randomNumberBox.getChildren().add(new HBox(new Label("Random:  "), randomTxt));

		Label nxtLabel = new Label("Previous Position");
		nxtLabel.setFont(Font.font(20));
		VBox nextPos = new VBox();
		nextPos.getChildren().add(nxtLabel);
		nextPos.getChildren().add(new HBox(new Label("Row      :  "), nextX));
		nextPos.getChildren().add(new HBox(new Label("Column :  "), nextY));

		Button button = new Button("Value Iteraton");
		button.setOnAction(new EventHandler<ActionEvent>() {
			public void handle(ActionEvent e) {

				mdp.valueIteration();
				pane.getChildren().retainAll(pane.getChildren());
				setUpGrid(pane);
			}
		});
		root.getChildren().addAll(currPos, action, randomNumberBox, nextPos, cb, button);
		return root;
	}

	private boolean checkLimits(int num, int limit) {
		return num >= 0 && num < limit;
	}


	private void attachEvents(Scene scene) {
		scene.setOnKeyPressed(new EventHandler<KeyEvent>() {
			public void handle(KeyEvent e) {

				double rand = random.nextDouble();

				randomTxt.setText(String.valueOf(rand));

				int newRow = player_row, newColumn = player_col;
				int direction = 1;
				if (e.getCode().equals(KeyCode.DOWN) || e.getCode().equals(KeyCode.RIGHT))
					direction = -1;

				if (e.getCode().equals(KeyCode.UP) || e.getCode().equals(KeyCode.DOWN)) {
					// for same direction
					row_column_Additions[0] = 1 * direction;
					row_column_Additions[1] = 0;

					// for direction in east
					row_column_Additions[2] = 0;
					row_column_Additions[3] = 1 * direction;

					// for direction in west
					row_column_Additions[4] = 0;
					row_column_Additions[5] = -1 * direction;

				} else if (e.getCode().equals(KeyCode.LEFT) || e.getCode().equals(KeyCode.RIGHT)) {
					// for same direction
					row_column_Additions[0] = 0;
					row_column_Additions[1] = -1 * direction;

					// for direction in east
					row_column_Additions[2] = 1 * direction;
					row_column_Additions[3] = 0;

					// for direction in west
					row_column_Additions[4] = -1 * direction;
					row_column_Additions[5] = 0;

				}
//				else if (e.getCode().equals(KeyCode.RIGHT)) {
//					//for same direction
//					row_column_Additions[0] = 0;
//					row_column_Additions[1] = 1;
//														
//					//for direction in east
//					row_column_Additions[2] = -1;
//					row_column_Additions[3] = 0;
//														
//					//for direction in west
//					row_column_Additions[4] = 1;
//					row_column_Additions[5] = 0;
//
//				}
//				else if (e.getCode().equals(KeyCode.DOWN)) {
//					//for same direction
//					row_column_Additions[0] = -1;
//					row_column_Additions[1] = 0;
//														
//					//for direction in east
//					row_column_Additions[2] = 0;
//					row_column_Additions[3] = -1;
//														
//					//for direction in west
//					row_column_Additions[4] = 0;
//					row_column_Additions[5] = 1;
//
//				}

				for (int i = 0, j = 0; i < 6; i += 2, j++) {
					if (rand <= decisionProbabilites[j]) {
						if (checkLimits(player_row + row_column_Additions[i], grid.getRows())
								&& checkLimits(player_col + row_column_Additions[i + 1], grid.getColumns())) {
							newRow = player_row + row_column_Additions[i];
							newColumn = player_col + row_column_Additions[i + 1];

						}
						break;
					}
				}

				nextX.setText(String.valueOf(player_row));
				nextY.setText(String.valueOf(player_col));

				grid.setValue(player_row, player_col, new Value(Constant.CELL_EMPTY, 0.0));
				grid.setValue(newRow, newColumn, new Value(Constant.CELL_PLAYER, 0.0));

				player_row = newRow;
				player_col = newColumn;

				currX.setText(player_row.toString());
				currY.setText(player_col.toString());

				pane.getChildren().removeAll(pane.getChildren());
				setUpGrid(pane);
			}
		});

		cb.setOnAction(x->{
			setUpGrid(pane);			
		});
	}

	private void setUpGrid(GridPane pane) {
		for (int row = grid.getRows() - 1, i = 0; row >= 0; row--, i++)
			for (int j = 0; j < grid.getColumns(); j++) {
				if (grid.getValue(row, j).getType().equals(Constant.CELL_EMPTY)) {
					pane.add(new EmptyCell(row, j, cb.getSelectionModel().getSelectedItem().getType(),
							grid.getValue(row, j)), j, i);
				} else if (grid.getValue(row, j).getType().equals(Constant.CELL_PLAYER)) {
					pane.add(new PlayerCell(row, j, cb.getSelectionModel().getSelectedItem().getType(),
							grid.getValue(row, j)), j, i);
					player_row = row;
					player_col = j;
					currX.setText(player_row.toString());
					currY.setText(player_col.toString());
				} else if (grid.getValue(row, j).getType().equals(Constant.CELL_WALL)) {
					pane.add(new WallCell(row, j, cb.getSelectionModel().getSelectedItem().getType(),
							grid.getValue(row, j)), j, i);
				} else if (grid.getValue(row, j).getType().equals(Constant.CELL_REWARD)) {
					pane.add(new RewardCell(row, j, cb.getSelectionModel().getSelectedItem().getType(),
							grid.getValue(row, j)), j, i);
				} else if (grid.getValue(row, j).getType().equals(Constant.CELL_PENALTY)) {
					pane.add(new PenaltyCell(row, j, cb.getSelectionModel().getSelectedItem().getType(),
							grid.getValue(row, j)), j, i);
				}

			}
	}

	public static void main(String[] areg) {
		launch(areg);
	}
}
