/**
 * Saier Ding(1011802)
 * @author saierd@student.unimelb.edu.au
 */

public class Knight extends Thread {
// enter -> sit -> release quest -> acquire quest -> stand -> exit -> set off -> complete quest -> enter... etc.
    private Hall greatHall;
    private Agenda agendaNew;
    private Agenda agendaComplete;
    private int id;
    Quest quest = null;

    public Knight(int number, Agenda newAgenda, Agenda completeAgenda, Hall greatHall) {
        this.id = number;
        this.agendaNew = newAgenda;
        this.agendaComplete = completeAgenda;
        this.greatHall = greatHall;
    }

    // get the id of the knight.
    public String toString(){
        return "Knight " + id;
    }
    // connect the knight with the specific quest.
    public void setupQuest(Quest quest){
        this.quest = quest;
    }

    // get the specific quest from the knight.
    public Quest getQuest(){
        return this.quest;
    }

    // knight sets of to complete Quest n!
    public synchronized void setOfComplete(){
        System.out.println(this.toString() + " sets of to complete " + quest.toString() + "!\n");
    }

    // knight completes the Quest.
    public synchronized void completeAgenda(){
        try{
            quest.completed = true;
            sleep(Params.getQuestingTime());
            System.out.println(this.toString() + " completes " + quest.toString() + ".\n");
        }catch (InterruptedException e){}
    }

    public void run() {
        while(!isInterrupted()) {
            try{
                greatHall.knightEnter(this);
                sleep(Params.getMinglingTime());
                greatHall.knightSit(this);
                // meeting begin
                while (!greatHall.isMeeting());
                if (quest != null && quest.completed == true ){
                    agendaComplete.releaseQuest(this);
                }
                agendaNew.acquireQuest(this);
                greatHall.knightStand(this);
                sleep(Params.getMinglingTime());
                // Meeting end
                greatHall.knightExit(this);
                setOfComplete();
                completeAgenda();
            }catch (InterruptedException e) {
                this.interrupt();
            }

        }
    }

}
