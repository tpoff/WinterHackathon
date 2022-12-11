using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Vuplex.WebView;

public class DynamicPageLoader : MonoBehaviour
{
    public WebViewPrefab view;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    public void loadPage(string pagePath)
    {

        view.WebView.LoadUrl(pagePath);
    }
}
