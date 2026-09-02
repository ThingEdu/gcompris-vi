import QtQuick 2.12
QtObject {
    property string name
    function exists(p) { return false }
    function read(p) { return "" }
    function write(d, p) { return false }
    function append(d, p) { return false }
    function rmpath(p) { return false }
    function mkpath(p) { return false }
}
