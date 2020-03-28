/**
 * Parameters for the questing knights simulator.
 *
 * @author ngeard@unimelb.edu.au
 *
 */

import java.util.Random;
import java.lang.Math;

class Params {
	
	static Random rnd = new Random();
	
	// number of knights in the simulator
    static final int NUM_KNIGHTS = 5;

    // average duration that knights spend mingling before and after meetings
    static final int MEAN_MINGLING_TIME = 200;

    // average duration that knights spend completing a quest
    static final int MEAN_QUESTING_TIME = 1200;
    
    // average interval between King Arthur leaving and re-entering the Hall
    static final int MEAN_KING_WAITING_TIME = 800;

    // duration between new quests being added
    static final int QUEST_ADDITION_TIME = 50;
    
    // duration between completed quests being removed
    static final int QUEST_REMOVAL_TIME = 20;
    
    // generate a random mingling duration
    static int getMinglingTime() {
        return (int) Math.max(0.0, rnd.nextGaussian() * 
        		MEAN_MINGLING_TIME / 6 + MEAN_MINGLING_TIME);
    }

    // generate a random questing duration
    static int getQuestingTime() {
        return (int) Math.max(0.0, rnd.nextGaussian() * 
        		MEAN_QUESTING_TIME / 6 + MEAN_QUESTING_TIME);
    }

    // generate a random interval for King Arthur to be away
    static int getKingWaitingTime() {
    	return (int) Math.max(0.0, (rnd.nextGaussian() * 
    			MEAN_KING_WAITING_TIME / 8) + MEAN_KING_WAITING_TIME);
    }

}
