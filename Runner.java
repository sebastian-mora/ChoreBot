
import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;

public class Runner {
    // Find your Account Sid and Token at twilio.com/console
    private static final String ACCOUNT_SID = "***REMOVED***";
    private static final String AUTH_TOKEN = "***REMOVED***";
    private static final String SENDER = "+***REMOVED***";

    private static ArrayList<Roommate> roommates = new ArrayList<>();
    private static ArrayList<Chore> toDochores = new ArrayList<>();
    private static ArrayList<Chore> finishdedchores = new ArrayList<>();


    public static void main(String[] args){

        initialize(ACCOUNT_SID,AUTH_TOKEN);
        Date date = java.util.Calendar.getInstance().getTime();

        while(true){
            if(date.getDate() != java.util.Calendar.getInstance().getTime().getDate()){
                date = java.util.Calendar.getInstance().getTime();
                assignChores(date);
            }


        }






    }

    public static void sendMessage(){

        Message message = Message.creator(
                new com.twilio.type.PhoneNumber("+***REMOVED***"),
                new com.twilio.type.PhoneNumber(SENDER),
                "Your message")
                .create();

        System.out.println("Message has been sent to: ");

    }

    private static void initialize(String ACCOUNT_SID, String AUTH_TOKEN){
        try {
            Twilio.init(ACCOUNT_SID, AUTH_TOKEN);

        }

        catch (Exception E){
            System.out.println("Program Failed on Start");
        }
    }

    private static void completeChore(Chore c, Roommate r){
        toDochores.remove(c);
        finishdedchores.add(c);
        r.setJobcompleted(true);
    }

    private static void assignChores(Date date){

    }


}