/**
 * A quest, with a unique id, to be assigned to a knight for completion
 * 
 * @author ngeard@unimelb.edu.au
 *
 */

public class Quest {

    // a unique identifier for this quest
    private int id;

    // the next ID to be allocated
    private static int nextId = 1;

    // a flag indicating whether the quest has been completed
    boolean completed;

    // create a new vessel with a given identifier
    private Quest(int id) {
        this.id = id;
        this.completed = false;
    }

    // get a new Quest instance with a unique identifier
    public static Quest getNewQuest() {
        return new Quest(nextId++);
    }

    // produce an identifying string for the quest
    public String toString() {
        return "Quest " + id;
    }

    public int getId(){
        return id;
    }

    public boolean isCompleted(){
        return completed;
    }
}