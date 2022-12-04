/*
 * Copyright (c) 2001-2022 Mathew A. Nelson and Robocode contributors
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * https://robocode.sourceforge.io/license/epl-v10.html
 */
package sample;


import robocode.DeathEvent;
import robocode.Robot;
import robocode.ScannedRobotEvent;
import static robocode.util.Utils.normalRelativeAngleDegrees;
import robocode.WinEvent;

import java.awt.*;


/**
 Father Bantay = Corners + Track Fire
 */
public class FatherBantay extends Robot {
	int others; // Number of other robots in the game
	static int corner = 0; // Which corner we are currently using
	// static so that it keeps it between rounds.
	boolean stopWhenSeeRobot = false; // See goCorner()

	/**
	 * run:  Corners' main run function.
	 */
	public void run() {
		// Set colors
		setBodyColor(Color.white);
		setGunColor(Color.white);
		setRadarColor(Color.white);
		setBulletColor(Color.red);
		setScanColor(Color.black);

		// Save # of other bots
		others = getOthers();

		// Move to a corner
		goCorner();

		// // Initialize gun turn speed to 10
		 int gunIncrement = 10;

		// // Spin gun back and forth
		 while (true) {
		 	for (int i = 0; i < 30; i++) {
		 		turnGunLeft(gunIncrement);
		 	}
		 	gunIncrement *= -1;
		 }
	}

	/**
	 * goCorner:  A very inefficient way to get to a corner.  Can you do better?
	 */
	public void goCorner() {
		// We don't want to stop when we're just turning...
		stopWhenSeeRobot = false;
		// turn to face the wall to the "right" of our desired corner.
		turnRight(normalRelativeAngleDegrees(corner - getHeading()));
		// Ok, now we don't want to crash into any robot in our way...
		stopWhenSeeRobot = true;
		// Move to that wall
		ahead(5000);
		// Turn to face the corner
		turnLeft(90);
		// Move to the corner
		ahead(5000);
		// Turn gun to starting point
		turnGunLeft(90);
	}

	public void onScannedRobot(ScannedRobotEvent e) {
		// Calculate exact location of the robot
		double absoluteBearing = getHeading() + e.getBearing();
		double bearingFromGun = normalRelativeAngleDegrees(absoluteBearing - getGunHeading());

		// If it's close enough, fire!
		if (Math.abs(bearingFromGun) <= 10) {
			turnGunRight(bearingFromGun);
			// We check gun heat here, because calling fire()
			// uses a turn, which could cause us to lose track
			// of the other robot.
			if (getGunHeat() == 0) {
				fire(Math.min(3 - Math.abs(bearingFromGun), getEnergy() - .1));
			}
		} // otherwise just set the gun to turn.
		// Note:  This will have no effect until we call scan()
		else {
			turnGunRight(bearingFromGun);
		}
		// Generates another scan event if we see a robot.
		// We only need to call this if the gun (and therefore radar)
		// are not turning.  Otherwise, scan is called automatically.
		if (bearingFromGun == 0) {
			scan();
		}
	}
	/**
	 * onScannedRobot:  Stop and fire!
	 */
	// public void onScannedRobot(ScannedRobotEvent e) {
	// 	// Should we stop, or just fire?
	// 	if (stopWhenSeeRobot) {
	// 		// Stop everything!  You can safely call stop multiple times.
	// 		stop();
	// 		// Call our custom firing method
	// 		smartFire(e.getDistance());
	// 		// Look for another robot.
	// 		// NOTE:  If you call scan() inside onScannedRobot, and it sees a robot,
	// 		// the game will interrupt the event handler and start it over
	// 		scan();
	// 		// We won't get here if we saw another robot.
	// 		// Okay, we didn't see another robot... start moving or turning again.
	// 		resume();
	// 	} else {
	// 		smartFire(e.getDistance());
	// 	}
	// }

	// /**
	//  * smartFire:  Custom fire method that determines firepower based on distance.
	//  *
	//  * @param robotDistance the distance to the robot to fire at
	//  */
	// public void smartFire(double robotDistance) {
	// 	if (robotDistance > 200 || getEnergy() < 15) {
	// 		fire(1);
	// 	} else if (robotDistance > 50) {
	// 		fire(2);
	// 	} else {
	// 		fire(3);
	// 	}
	// }

	/**
	 * onDeath:  We died.  Decide whether to try a different corner next game.
	 */
	public void onDeath(DeathEvent e) {
		// Well, others should never be 0, but better safe than sorry.
		if (others == 0) {
			return;
		}

		// If 75% of the robots are still alive when we die, we'll switch corners.
		if (getOthers() / (double) others >= .75) {
			corner += 90;
			if (corner == 270) {
				corner = -90;
			}
			out.println("I died and did poorly... switching corner to " + corner);
		} else {
			out.println("I died but did well.  I will still use corner " + corner);
		}
	}

    public void onWin(WinEvent e) {
	// Victory dance
		turnRight(36000);
	}
}

