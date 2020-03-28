/**
 * Saier Ding(1011802)
 * @author saierd@student.unimelb.edu.au
 */

import java.util.HashMap;
import java.util.LinkedList;


public class Agenda {

    private String type;
    LinkedList<Quest> questMap;

    public Agenda(String Type){
        this.type = Type;
        this.questMap = new LinkedList<>();
    }

    // create Quest and added it to New Agenda.
    public synchronized void addNew(Quest newQuest) {
        // monitor that the capacity of the agenda is 5
        while (questMap.size() >= 5){
            try {
                wait();
            } catch (InterruptedException e) {
            }
        }
        questMap.add(newQuest);
        System.out.println(newQuest.toString() + " added to " + type + ".\n");
        notifyAll();
    }

    // remove Quest from Complete Agenda.
    public synchronized void removeComplete(){
        // monitor that the quest list have enough quest
        while (questMap.isEmpty()){
            try{
                wait();
            }
            catch(InterruptedException e){}
        }
        Quest removedQuest = questMap.removeFirst();
        System.out.println(removedQuest.toString() + " removed from " + type + ".\n");
        notifyAll();
    }

    // Knight acquire Quest in meeting.
    public synchronized void acquireQuest(Knight knight){
        // monitor that if there are enough Quest to assign.
        while (questMap.isEmpty()){
            try{
                wait();
            }
            catch (InterruptedException e){}
        }
        Quest acquireQuest = questMap.removeFirst();
        knight.setupQuest(acquireQuest);
        notifyAll();
        System.out.println(knight.toString() + " acquires to " + acquireQuest.toString() + ".\n");
    }

    // Knight release Quest in meeting.
    public synchronized void releaseQuest(Knight knight){
        // monitor that if agenda number is beyond 5.
        while (questMap.size() >= 5){
            try{
                wait();
            }
            catch (InterruptedException e){}
        }
        questMap.add(knight.getQuest());
        notifyAll();
        System.out.println(knight.toString() + " releases to " + knight.getQuest().toString() + ".\n");
    }

}
