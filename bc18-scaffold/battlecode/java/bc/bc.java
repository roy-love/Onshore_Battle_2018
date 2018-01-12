/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 3.0.12
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package bc;

public class bc {
  public static Planet bcPlanetOther(Planet arg0) {
    return Planet.swigToEnum(bcJNI.bcPlanetOther(arg0.swigValue()));
  }

  public static String bcPlanetDebug(Planet arg0) {
    return bcJNI.bcPlanetDebug(arg0.swigValue());
  }

  public static boolean bcPlanetEq(Planet arg0, Planet other) {
    return bcJNI.bcPlanetEq(arg0.swigValue(), other.swigValue());
  }

  public static Planet bcPlanetFromJson(String s) {
    return Planet.swigToEnum(bcJNI.bcPlanetFromJson(s));
  }

  public static String bcPlanetToJson(Planet arg0) {
    return bcJNI.bcPlanetToJson(arg0.swigValue());
  }

  public static int bcDirectionDx(Direction arg0) {
    return bcJNI.bcDirectionDx(arg0.swigValue());
  }

  public static int bcDirectionDy(Direction arg0) {
    return bcJNI.bcDirectionDy(arg0.swigValue());
  }

  public static boolean bcDirectionIsDiagonal(Direction arg0) {
    return bcJNI.bcDirectionIsDiagonal(arg0.swigValue());
  }

  public static Direction bcDirectionOpposite(Direction arg0) {
    return Direction.swigToEnum(bcJNI.bcDirectionOpposite(arg0.swigValue()));
  }

  public static Direction bcDirectionRotateLeft(Direction arg0) {
    return Direction.swigToEnum(bcJNI.bcDirectionRotateLeft(arg0.swigValue()));
  }

  public static Direction bcDirectionRotateRight(Direction arg0) {
    return Direction.swigToEnum(bcJNI.bcDirectionRotateRight(arg0.swigValue()));
  }

  public static Direction bcDirectionFromJson(String s) {
    return Direction.swigToEnum(bcJNI.bcDirectionFromJson(s));
  }

  public static String bcDirectionToJson(Direction arg0) {
    return bcJNI.bcDirectionToJson(arg0.swigValue());
  }

  public static MapLocation bcMapLocationFromJson(String s) {
    long cPtr = bcJNI.bcMapLocationFromJson(s);
    return (cPtr == 0) ? null : new MapLocation(cPtr, true);
  }

  public static Location bcLocationNewOnMap(MapLocation map_location) {
    long cPtr = bcJNI.bcLocationNewOnMap(MapLocation.getCPtr(map_location), map_location);
    return (cPtr == 0) ? null : new Location(cPtr, true);
  }

  public static Location bcLocationNewInGarrison(int id) {
    long cPtr = bcJNI.bcLocationNewInGarrison(id);
    return (cPtr == 0) ? null : new Location(cPtr, true);
  }

  public static Location bcLocationNewInSpace() {
    long cPtr = bcJNI.bcLocationNewInSpace();
    return (cPtr == 0) ? null : new Location(cPtr, true);
  }

  public static Location bcLocationFromJson(String s) {
    long cPtr = bcJNI.bcLocationFromJson(s);
    return (cPtr == 0) ? null : new Location(cPtr, true);
  }

  public static Team bcTeamFromJson(String s) {
    return Team.swigToEnum(bcJNI.bcTeamFromJson(s));
  }

  public static String bcTeamToJson(Team arg0) {
    return bcJNI.bcTeamToJson(arg0.swigValue());
  }

  public static Player bcPlayerFromJson(String s) {
    long cPtr = bcJNI.bcPlayerFromJson(s);
    return (cPtr == 0) ? null : new Player(cPtr, true);
  }

  public static UnitType bcUnitTypeFromJson(String s) {
    return UnitType.swigToEnum(bcJNI.bcUnitTypeFromJson(s));
  }

  public static String bcUnitTypeToJson(UnitType arg0) {
    return bcJNI.bcUnitTypeToJson(arg0.swigValue());
  }

  public static long bcUnitTypeFactoryCost(UnitType arg0) {
    return bcJNI.bcUnitTypeFactoryCost(arg0.swigValue());
  }

  public static long bcUnitTypeBlueprintCost(UnitType arg0) {
    return bcJNI.bcUnitTypeBlueprintCost(arg0.swigValue());
  }

  public static long bcUnitTypeReplicateCost(UnitType arg0) {
    return bcJNI.bcUnitTypeReplicateCost(arg0.swigValue());
  }

  public static long bcUnitTypeValue(UnitType arg0) {
    return bcJNI.bcUnitTypeValue(arg0.swigValue());
  }

  public static Unit bcUnitFromJson(String s) {
    long cPtr = bcJNI.bcUnitFromJson(s);
    return (cPtr == 0) ? null : new Unit(cPtr, true);
  }

  public static PlanetMap bcPlanetMapFromJson(String s) {
    long cPtr = bcJNI.bcPlanetMapFromJson(s);
    return (cPtr == 0) ? null : new PlanetMap(cPtr, true);
  }

  public static Delta bcDeltaFromJson(String s) {
    long cPtr = bcJNI.bcDeltaFromJson(s);
    return (cPtr == 0) ? null : new Delta(cPtr, true);
  }

  public static StartGameMessage bcStartGameMessageFromJson(String s) {
    long cPtr = bcJNI.bcStartGameMessageFromJson(s);
    return (cPtr == 0) ? null : new StartGameMessage(cPtr, true);
  }

  public static TurnMessage bcTurnMessageFromJson(String s) {
    long cPtr = bcJNI.bcTurnMessageFromJson(s);
    return (cPtr == 0) ? null : new TurnMessage(cPtr, true);
  }

  public static StartTurnMessage bcStartTurnMessageFromJson(String s) {
    long cPtr = bcJNI.bcStartTurnMessageFromJson(s);
    return (cPtr == 0) ? null : new StartTurnMessage(cPtr, true);
  }

  public static ViewerMessage bcViewerMessageFromJson(String s) {
    long cPtr = bcJNI.bcViewerMessageFromJson(s);
    return (cPtr == 0) ? null : new ViewerMessage(cPtr, true);
  }

  public static ViewerKeyframe bcViewerKeyframeFromJson(String s) {
    long cPtr = bcJNI.bcViewerKeyframeFromJson(s);
    return (cPtr == 0) ? null : new ViewerKeyframe(cPtr, true);
  }

  public static ErrorMessage bcErrorMessageFromJson(String s) {
    long cPtr = bcJNI.bcErrorMessageFromJson(s);
    return (cPtr == 0) ? null : new ErrorMessage(cPtr, true);
  }

  public static AsteroidStrike bcAsteroidStrikeFromJson(String s) {
    long cPtr = bcJNI.bcAsteroidStrikeFromJson(s);
    return (cPtr == 0) ? null : new AsteroidStrike(cPtr, true);
  }

  public static AsteroidPattern bcAsteroidPatternFromJson(String s) {
    long cPtr = bcJNI.bcAsteroidPatternFromJson(s);
    return (cPtr == 0) ? null : new AsteroidPattern(cPtr, true);
  }

  public static OrbitPattern bcOrbitPatternFromJson(String s) {
    long cPtr = bcJNI.bcOrbitPatternFromJson(s);
    return (cPtr == 0) ? null : new OrbitPattern(cPtr, true);
  }

  public static GameMap bcGameMapTestMap() {
    long cPtr = bcJNI.bcGameMapTestMap();
    return (cPtr == 0) ? null : new GameMap(cPtr, true);
  }

  public static GameMap bcGameMapFromJson(String s) {
    long cPtr = bcJNI.bcGameMapFromJson(s);
    return (cPtr == 0) ? null : new GameMap(cPtr, true);
  }

  public static long maxLevel(UnitType branch) {
    return bcJNI.maxLevel(branch.swigValue());
  }

  public static long costOf(UnitType branch, long level) {
    return bcJNI.costOf(branch.swigValue(), level);
  }

  public static ResearchInfo bcResearchInfoFromJson(String s) {
    long cPtr = bcJNI.bcResearchInfoFromJson(s);
    return (cPtr == 0) ? null : new ResearchInfo(cPtr, true);
  }

  public static RocketLanding bcRocketLandingFromJson(String s) {
    long cPtr = bcJNI.bcRocketLandingFromJson(s);
    return (cPtr == 0) ? null : new RocketLanding(cPtr, true);
  }

  public static RocketLandingInfo bcRocketLandingInfoFromJson(String s) {
    long cPtr = bcJNI.bcRocketLandingInfoFromJson(s);
    return (cPtr == 0) ? null : new RocketLandingInfo(cPtr, true);
  }

  public static GameController bcGameControllerNewManager(GameMap map) {
    long cPtr = bcJNI.bcGameControllerNewManager(GameMap.getCPtr(map), map);
    return (cPtr == 0) ? null : new GameController(cPtr, true);
  }

}
