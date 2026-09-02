import QtQuick 2.12
Text {
    property int tinySize: 8
    property int smallSize: 12
    property int regularSize: 16
    property int mediumSize: 20
    property int largeSize: 26
    property int hugeSize: 34
    property int fontSize: regularSize
    font.pixelSize: fontSize
}
