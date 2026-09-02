pragma Singleton
import QtQuick 2.12
QtObject {
    function haveLocalResource(p) { return true }
    function downloadResource(p) { return false }
    function areVoicesRegistered() { return true }
    function getVoicesResourceForLocale(l) { return "" }
}
