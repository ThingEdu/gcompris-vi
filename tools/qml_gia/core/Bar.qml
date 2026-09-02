import QtQuick 2.12
Item {
    property var content          // GCompris thật: property BarEnumContent content
    property int level: 1
    signal helpClicked(); signal homeClicked(); signal reloadClicked()
    signal previousLevelClicked(); signal nextLevelClicked()
}
