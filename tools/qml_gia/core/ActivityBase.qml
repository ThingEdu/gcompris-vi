import QtQuick 2.12
Item {
    id: activity
    property Item main: activity
    property Component pageComponent
    property QtObject audioEffects: QtObject { function play(s) {} }
    signal start()
    signal stop()
    function home() {}
    function displayDialog(d) {}
    property int tinySize: 8
    property int smallSize: 12
    property int regularSize: 16
    property int mediumSize: 20
    property int largeSize: 26
    property int hugeSize: 34
    Loader { anchors.fill: parent; sourceComponent: activity.pageComponent }
}
