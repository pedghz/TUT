using UnityEngine;
using UnityEngine.SceneManagement;

public class GameManager : Singleton<GameManager>
{
	int health = 5;
	int points = 0;
    int savedPoints = 0;

    protected GameManager() { }

    public void TakeDamage(int amount = 1)
    {
        health -= amount;
        UpdateHealth();

        if (health > 0)
            RestartLevel();
        else
            RestartGame();

        ResetPoints();
    }

    public int GetHealth()
    {
        return health;
    }

    void UpdateHealth()
    {
        GameObject healthObject = GameObject.Find("Health");

        if (!healthObject)
            return;

        Health healthController = healthObject.GetComponent<Health>();
        healthController.UpdateHealth();
    }

    void ResetHealth()
    {
        health = 5;
        UpdateHealth();
    }

    public int GetPoints()
    {
        return points;
    }

    public void AddPoints(int amount = 1)
    {
        points += amount;
        UpdatePoints();
    }

    public void ResetPoints()
    {
        points = savedPoints;
        UpdatePoints();
    }

    void UpdatePoints()
    {
        GameObject pointsObject = GameObject.Find("Points");

        if (!pointsObject)
            return;
        
        Points pointsController = pointsObject.GetComponent<Points>();
        pointsController.UpdatePoints();
    }

    public void LoadLevel(string level)
    {
        if (level == "MainMenu")
        {
            points = 0;
        }
        ResetHealth();
        savedPoints = points;
        SceneManager.LoadScene(level);
    }

    void RestartLevel()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }

    void RestartGame()
    {
        ResetHealth();
        savedPoints = 0;
        SceneManager.LoadScene(0);
    }

    public string GetVar(string var)
    {
        if(var == "scr")
        {
            return GetPoints().ToString();
        }
        if(var == "nme")
        {
            if((PlayerPrefs.HasKey("PlayerName")))
            {
                return PlayerPrefs.GetString("PlayerName");
            }
            return "Boris";
        }
        return "[ERROR: No value found]";
    }
}
