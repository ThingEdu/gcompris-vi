pragma Singleton
import QtQuick 2.12
QtObject {
    property int applicationWidth: 1920
    property real ratio: 1.0
    property real fontRatio: 1.0
    property bool isMobile: false
    property bool useOpenGL: false
    property string localeShort: "vi"
    function getResourceDataPath(p) { return p }
    function getAudioFilePath(p) { return p }
    function getAudioFilePathForLocale(p, l) { return p }
    function getLocaleFilePath(p) { return p }
    function screenshot(p) {}
}
