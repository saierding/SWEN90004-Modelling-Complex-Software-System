/**
 * Saier Ding(1011802)
 * @author saierd@student.unimelb.edu.au
 */

import java.util.HashMap;
import java.util.Set;


public class Hall {
    private String name;
    public boolean isMeeting = false;
    public boolean isKingEnter = false;
    private Agenda agendaNew;
    private Agenda agendaComplete;
    HashMap<Knight,Boolean> isKnightAllSit = new HashMap<Knight,Boolean>();

    public Hall (String name, Agenda agendaNew, Agenda agendaComplete) {
        this.name = name;
        this.agendaNew = agendaNew;
        this.agendaComplete = agendaComplete;
    }

    // king enter the great hall.
    public synchronized void kingEnter(KingArthur king) {
        isKingEnter = true;
        System.out.println("King Arthur enters the " + name + ".\n");
    }

    // king exit the great hall.
    public synchronized void kingExit(KingArthur king) {
        isKingEnter = false;
        System.out.println("king Arthur exits the " + name + ".\n");
        notifyAll();
    }

    // knight enter great hall.
    public synchronized void knightEnter(Knight knight) {
        while (isKingEnter){
            try{
                wait();
            }catch(InterruptedException e){}
        }
        isKnightAllSit.put(knight,false);
        System.out.println(knight.toString() + " enters " + name + ".\n");
    }

    // knight exit great hall.
    public synchronized void knightExit(Knight knight) {
        while (isKingEnter){
            try{
                wait();
            }catch(InterruptedException e){}
        }
        isKnightAllSit.remove(knight,false);
        notifyAll();
        System.out.println(knight.toString() + " exits from " + name + ".\n");
    }

    // knight sit at the Round Table.
    public synchronized void knightSit(Knight knight) {
        isKnightAllSit.put(knight,true);
        System.out.println(knight.toString() + " sits at the Round Table " + ".\n");
        notifyAll();
    }

    // knight stand from the Round Table.
    public synchronized void  knightStand(Knight knight) {
        isKnightAllSit.put(knight, false);
        System.out.println(knight.toString() + " stands from the Round Table" + ".\n");
        notifyAll();
    }

    // is all the knight sited
    public synchronized boolean isAllKnightSit(){
        Set<Knight> keys=isKnightAllSit.keySet();
        for(Knight key : keys){
            boolean value = isKnightAllSit.get(key);
            if(value == false){
                return false;
            }
        }
        return true;
    }

    // is all the knight stand
    public synchronized boolean isAllKnightStand() {
        Set<Knight> keys=isKnightAllSit.keySet();
        for(Knight key : keys){
            boolean value = isKnightAllSit.get(key);
            if(value == true){
                return false;
            }
        }
        return true;
    }

    // is meeting begins
    public synchronized void meetingBegin() {
        while(!isAllKnightSit()) {
            try {
                wait();
            }
            catch (InterruptedException e) {}
        }
        this.isMeeting = true;
        System.out.println("Meeting begins!");
    }

    // is meeting ends
    public synchronized void meetingEnd() {
        while(!isAllKnightStand()) {
            try {
                wait();
            }
            catch (InterruptedException e) {}
        }
        this.isMeeting = false;
        System.out.println("Meeting ends!");
    }

    public synchronized boolean isMeeting(){
        return isMeeting;
    }

}
