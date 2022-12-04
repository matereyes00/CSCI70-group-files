package Contestants;
import robocode.*;
import java.awt.*;
import java.awt.Color;

import robocode.HitByBulletEvent;
import robocode.HitRobotEvent;
import robocode.Robot;
import robocode.ScannedRobotEvent;
import static robocode.util.Utils.normalRelativeAngleDegrees;
import robocode.AdvancedRobot;


// API help : https://robocode.sourceforge.io/docs/robocode/robocode/Robot.html

/**
 * Double007Bot - a robot by 
 * @author Martina Therese Reyes
 * This is a robot that actively avoids
 */
public class Double007Bot extends AdvancedRobot {
	boolean movingForward;
	private byte moveDirection = 1;
	
	/**
	 * run: Double007Bot's default behavior
	 */
	public void run() {
		// Initialization of the robot should be put here

		// setColors(Color.red,Color.blue,Color.green); // body,gun,radar
		setBodyColor(new Color(45,49,66));
		setGunColor(new Color(0, 150, 50));
		setRadarColor(new Color(247,197,159));
		
		setBulletColor(new Color(255, 255, 100));
		setScanColor(new Color(130,74,99));

		// Robot main loop
		while(true) {
			// Limit our speed to 5
			setMaxVelocity(5);
			// Tell the game we will want to move ahead 40000 -- some large number
			setAhead(40000);
			
			// setTurnLeft(360);
			ahead(100); // Move ahead 100
			setTurnRight(90);
			
		}
	}

	/**
	 * onScannedRobot: What to do when you see another robot
	 */
	public void onScannedRobot(ScannedRobotEvent e) {
		// Calculate exact location of the robot
		double absoluteBearing = getHeading() + e.getBearing();
		double bearingFromGun = normalRelativeAngleDegrees(absoluteBearing - getGunHeading());
		double bearingFromRadar = normalRelativeAngleDegrees(absoluteBearing - getRadarHeading());
		
		//Spiral around our enemy. 90 degrees would be circling it (parallel at all times)
		// 80 and 100 make that we move a bit closer every turn.
		if (movingForward){
			setTurnRight(normalRelativeAngleDegrees(e.getBearing() + 80));
		} else {
			setTurnRight(normalRelativeAngleDegrees(e.getBearing() + 100));
		}

		// If it's close enough, fire!
		if (Math.abs(bearingFromGun) <= 4) {
			// setTurnGunRight(bearingFromGun); 
			// We can easily turn the gun toward our opponent when we scan him by using a formula 
			setTurnGunRight(getHeading() - getGunHeading() + e.getBearing());
			setTurnRadarRight(bearingFromRadar); // keep the radar focussed on the enemy
			setTurnRight(normalRelativeAngleDegrees(e.getBearing() + 80)); // keep moving while firing

			// We check gun heat here, because calling fire()
			// uses a turn, which could cause us to lose track
			// of the other robot.
			
			// The close the enmy robot, the bigger the bullet. 
			// The more precisely aimed, the bigger the bullet.
			// Don't fire us into disability, always save .1
			if (getGunHeat() == 0 && getEnergy() > .2) {
				fire(Math.min(4.5 - Math.abs(bearingFromGun) / 2 - e.getDistance() / 250, getEnergy() - .1));
			} 
		} // otherwise just set the gun to turn.
		else {
			setTurnGunRight(bearingFromGun);
			setTurnRadarRight(bearingFromRadar);
		}
		// Generates another scan event if we see a robot.
		// We only need to call this if the radar
		// is not turning.  Otherwise, scan is called automatically.
		if (bearingFromGun == 0) {
			scan();
		}
	}		
	
	/**
	 * avoid:  Switch from ahead to back &amp; vice versa
	 */
	public void avoid() {
		if (movingForward) {
			setBack(100);
			setTurnRight(180);
			movingForward = false;
		} else {
			setAhead(100);
			setTurnLeft(180);
			movingForward = true;
		}
	}

	/**
	 * smartFire:  Custom fire method that determines firepower based on distance.
	 *
	 * @param robotDistance the distance to the robot to fire at
	 */
	public void smartFire(double robotDistance) {
		if (robotDistance > 200 || getEnergy() < 15) {
			fire(1);
		} else if (robotDistance > 50) {
			fire(2);
		} else {
			fire(3);
		}
	}

	/**
	 * onHitByBullet: What to do when you're hit by a bullet
	 */
	public void onHitByBullet(HitByBulletEvent e) {
		// Turn perpendicular to the bullet, and move a bit.
		turnRight(normalRelativeAngleDegrees(90 - (getHeading() - e.getHeading())));
		turnGunRight(90);
		// Start moving (and turning)
		back(10000);
	}

	/**
	 * onHitRobot: Back up!
	 */
	public void onHitRobot(HitRobotEvent e) {
		double absoluteBearing = getHeading() + e.getBearing();
		double turnGunAmt = normalRelativeAngleDegrees(e.getBearing() + getHeading() - getGunHeading());
		double bearingFromRadar = normalRelativeAngleDegrees(absoluteBearing - getRadarHeading());

		setTurnGunRight(getHeading() - getGunHeading() + e.getBearing());
		turnGunRight(turnGunAmt);
		setTurnRight(normalRelativeAngleDegrees(e.getBearing() + 80)); // keep moving while firing
		setTurnRadarRight(bearingFromRadar); // keep the radar focussed on the enemy

		// Call our custom firing method
		smartFire(bearingFromRadar);
	}
	
	/**
	 * onHitWall: What to do when you hit a wall
	 */
	public void onHitWall(HitWallEvent e) {
		// Bounce off!
		avoid();
		// setTurnLeft(180);
		setTurnRight(180);
	}	
}
