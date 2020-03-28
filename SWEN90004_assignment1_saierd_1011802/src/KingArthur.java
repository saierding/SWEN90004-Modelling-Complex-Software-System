/**
 * Saier Ding(1011802)
 * @author saierd@student.unimelb.edu.au
 */

public class KingArthur extends Thread{

    private Hall greatHall;
    public boolean isMeeting;
    public boolean isHall;

    public KingArthur(Hall greatHall) {
        this.greatHall = greatHall;
    }

    public void run() {
        while(!isInterrupted()) {
            try{
                sleep(Params.getKingWaitingTime());
            } catch (InterruptedException e) {}
            greatHall.kingEnter(this);
            greatHall.meetingBegin();
            greatHall.meetingEnd();
            greatHall.kingExit(this);
        }
    }

}
