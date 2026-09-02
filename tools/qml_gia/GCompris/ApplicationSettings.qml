pragma Singleton
import QtQuick 2.12
QtObject {
    property bool isAudioVoicesEnabled: true
    property bool isAudioEffectsEnabled: true
    property bool isFullscreen: true
    property bool sectionVisible: true
    property bool isBarHidden: false
    property int baseFontSize: 0
    property real fontLetterSpacing: 0
    property string locale: "vi_VN.UTF-8"
    property string font: "Andika-R.ttf"
    property bool isEmbeddedFont: true
    property int fontCapitalization: 0
    property bool isVirtualKeyboard: false
    property bool isAutomaticDownloadsEnabled: false
    property int filterLevelMin: 1
    property int filterLevelMax: 6
    property bool useExternalWordset: false
    function notifyActivityLevels(a, b, c) {}
    function setFavorite(a, b) {}
}
