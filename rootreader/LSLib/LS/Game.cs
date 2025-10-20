namespace rootreader.LSLib.LS;
public enum Game // I can probably remove this again, the error it shows doesn't actually break anything. At least if you're importing BG3. May break other games. Don't have any relevant files to test yet though. Leaving here for the time being.
{
    DivinityOriginalSin = 0,
    DivinityOriginalSinEE = 1,
    DivinityOriginalSin2 = 2,
    DivinityOriginalSin2DE = 3,
    BaldursGate3 = 4,
    Unset = 5
};

public static class GameEnumExtensions
{
    public static bool IsFW3(this Game game)
    {
        return game != Game.DivinityOriginalSin
            && game != Game.DivinityOriginalSinEE;
    }
}
