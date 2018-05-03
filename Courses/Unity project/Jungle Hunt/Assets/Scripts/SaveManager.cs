using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SaveManager : MonoBehaviour
{
    public InputField DataField;

	void Start ()
	{
	    if (PlayerPrefs.HasKey("PlayerName"))
	        DataField.text = PlayerPrefs.GetString("PlayerName");
	}

    public void SaveInputFieldString(string key)
    {
        PlayerPrefs.SetString(key, DataField.text);
        PlayerPrefs.Save();
    }
}
