/**
 * Consumes completed quests from an agenda.
 *
 * @author ngeard@unimelb.edu.au
 *
 */

public class Consumer extends Thread {

    // the agenda from which completed quests are removed
    private Agenda agenda;

    // creates a new consumer for the given agenda
    Consumer(Agenda newAgenda) {
        this.agenda = newAgenda;
    }

    // repeatedly collect completed quests from the agenda
    public void run() {
        while (!isInterrupted()) {
            try {
                // remove a quest that is complete
                agenda.removeComplete();

                // let some time pass before the next quest is removed
                sleep(Params.QUEST_REMOVAL_TIME);
            }
            catch (InterruptedException e) {
                this.interrupt();
            }
        }
    }
}
