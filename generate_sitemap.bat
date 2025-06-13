@echo off
echo ^<?xml version="1.0" encoding="UTF-8"?^> > sitemap.xml
echo ^<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"^> >> sitemap.xml
for /r %%i in (*.html) do (
    set "relativePath=%%i"
    set "relativePath=!relativePath:%CD%\=!"
    echo   ^<url^> >> sitemap.xml
    echo     ^<loc^>https://github.com/bizcircle2/healthmedic/blob/main/!relativePath!^</loc^> >> sitemap.xml
    echo   ^</url^> >> sitemap.xml
)
echo ^</urlset^> >> sitemap.xml