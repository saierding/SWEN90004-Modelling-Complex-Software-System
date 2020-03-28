/**
 * The top-level component of the questing knights simulator.
 *
 * It is responsible for:
 *  - creating all the components of the system;
 *  - starting all of the processes;
 *
 * @author ngeard@unimelb.edu.au
 *
 */

public class Main {

    public static void main(String [] args) throws InterruptedException {

        // generate the hall and quest agendas
        Agenda agendaNew = new Agenda("New Agenda");
        Agenda agendaComplete = new Agenda("Complete Agenda");
        Hall greatHall = new Hall("Great Hall", agendaNew, agendaComplete);

        // generate the producer, consumer and king arthur processes
        Producer producer = new Producer(agendaNew);
        Consumer consumer = new Consumer(agendaComplete);
        KingArthur kingArthur = new KingArthur(greatHall);

        // create an array of knights
        Knight[] knights = new Knight[Params.NUM_KNIGHTS];

        // generate and start the individual knight processes
        for (int i = 0; i < Params.NUM_KNIGHTS; i++) {
            knights[i] = new Knight(i + 1, agendaNew, agendaComplete, greatHall);
            knights[i].start();
        }

        // start the remaining processes
        producer.start();
        consumer.start();
        kingArthur.start();

        // join all processes
        for (int i = 0; i < Params.NUM_KNIGHTS; i++) {
            knights[i].join();
        }
        producer.join();
        consumer.join();
        kingArthur.join();
    }
}