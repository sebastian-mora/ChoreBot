

public class Roommate {

    private String name;
    private String day1;
    private String day2;
    private String num;
    private Boolean jobcompleted = false;

    public Roommate(String name, String day1, String day2, String num) {
        this.name = name;
        this.day1 = day1;
        this.day2 = day2;
        this.num = num;
    }

    public String getName() {
        return name;
    }

    public String getDay1() {
        return day1;
    }



    public String getDay2() {
        return day2;
    }

    public void setJobcompleted(Boolean jobcompleted) {
        this.jobcompleted = jobcompleted;
    }
}