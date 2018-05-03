using UnityEngine;
using UnityEngine.UI;

public class Points : MonoBehaviour
{
    public Text PointsText;

    void Start()
    {
        UpdatePoints();
    }

    public void UpdatePoints()
    {
        PointsText.text = GameManager.Instance.GetPoints().ToString();
    }
}
