import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class FileHandler {

    private static final String CHORESTODO = "C:\\Users\\Seb\\IdeaProjects\\ChoreBot\\src\\chorelist.txt" ;
    private static final String CHORESCOMP = "C:\\Users\\Seb\\IdeaProjects\\ChoreBot\\src\\Runner.java";
    private static final String ROOMMATES = "C:\\Users\\Seb\\IdeaProjects\\ChoreBot\\src\\Numbers.csv";

    public ArrayList<Roommate> parseRoommates(){
        ArrayList<Roommate> roommates = new ArrayList<>();
        try {
            File file = new File(ROOMMATES);
            FileReader fileReader = new FileReader(file);
            BufferedReader bufferedReader = new BufferedReader(fileReader);
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                List<String> list = new ArrayList<String>(Arrays.asList(line.split(",")));
                roommates.add(new Roommate(list.get(0), list.get(1), list.get(2), list.get(3)));

            }
            fileReader.close();
            bufferedReader.close();
        }
        catch (IOException e){}



        return roommates;
    }

    public ArrayList<Chore> parseChores() {
        ArrayList<Chore> chores = new ArrayList<>();
        try {
            File file = new File(CHORESTODO);
            FileReader fileReader = new FileReader(file);
            BufferedReader bufferedReader = new BufferedReader(fileReader);
            String line;

            while ((line = bufferedReader.readLine()) != null) {

                chores.add(new Chore(line));
            }
            fileReader.close();
            bufferedReader.close();
        }
        catch (IOException e) { }

        return chores;
    }

    public void completeChore(Chore c, Roommate r){

        try {
            PrintWriter pw = new PrintWriter("C:\\Users\\Seb\\IdeaProjects\\ChoreBot\\src\\CompletedChores.txt");
            BufferedReader br1 = new BufferedReader(new FileReader(CHORESTODO));
            String line1 = br1.readLine();

            while(line1 != null){
                if(!line1.equals(c.getDescription())){

                }
            }


        } catch (IOException e) {
            e.printStackTrace();
        }


    }


}
