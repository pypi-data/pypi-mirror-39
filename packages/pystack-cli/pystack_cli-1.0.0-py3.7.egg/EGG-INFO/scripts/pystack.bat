@ECHO OFF

SET PORT=3571
SET COMMAND=%1
SET TYPE=%2
SET NAME=%3
SET URL=%4
SET GIT_REPOSITORY="https://github.com/zoltancsontos/pystack-framework.git" %NAME%
SET CURRENT_INSTALLATION_FILE=%cd%\pystack.py

IF NOT DEFINED COMMAND (SET COMMAND=help)
IF NOT DEFINED URL (SET URL=none)
IF NOT DEFINED NAME (SET NAME=none)

IF "%COMMAND%"=="create" (
    IF "%TYPE%"=="app" (
        git clone %GIT_REPOSITORY%
        cd %NAME%
        pip3 install -r requirements.txt
        rm -rf .git
        ECHO.
        ECHO ==========================================================================
        ECHO                        New PyStack app created
        ECHO App path: %cd%
        ECHO ==========================================================================
        ECHO.
        GOTO exit
    ) ELSE (
        IF EXIST "%CURRENT_INSTALLATION_FILE%" GOTO ForwardToPyStack
        REM ELSE GOTO PackageNotInstalled
    )
)
IF "%COMMAND%"=="run" (
   python pystack.py %*
   GOTO exit
)
IF "%COMMAND%"=="help" (
    ECHO.
    ECHO ==========================================================================================
    ECHO                              PyStack Framework v1.0
    ECHO ==========================================================================================
    ECHO.
    ECHO List of CLI options:
    ECHO.
    ECHO pystack create app appName - creates a new pystack application with the specified name
    ECHO pystack run --port=port - runs the application on the specified port
    ECHO pystack create page PageName page-url - creates a page
    ECHO pystack create resource ResourceName resource-url - creates a standard rest api
    ECHO.
) ELSE (
    GOTO MissingArgument
)

:ForwardToPyStack
    IF "%TYPE%" == "page" OR "%TYPE%" == "resource" (
        IF NOT "%NAME%" == "none" (
            IF NOT "%URL%" == "none" (
                ECHO Creating new %TYPE% called %NAME%, accessible on: %URL%
                python pystack.py %*
                GOTO exit
            )
        )
    )
    GOTO :MissingArgument

:MissingArgument
    ECHO.
    ECHO ERROR: Missing or misspelled mandatory argument
    GOTO exit

:PackageNotInstalled
    ECHO.
    ECHO ERROR: Not a PyStack application
    GOTO exit

:exit