/* GCompris - Đối Đôi Làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Linh vật Tux trong bộ hình là bản vẽ lại; linh vật Linux gốc của Larry Ewing.
 */
import GCompris 1.0

ActivityInfo {
  name: "lang_doidoi/Lang_doidoi.qml"
  difficulty: 2
  icon: "lang_doidoi/resource/hinh/01-neo_tre.svg"
  author: "ThingEdu &lt;tuan@rogo.com.vn&gt;"
  title: qsTr("Đối Đôi Làng")
  description: qsTr("Bộ bài 57 hình của Làng Maker: hai thẻ bất kỳ luôn có đúng một hình giống nhau.")
  goal: qsTr("Nhìn nhanh, gọi to, tìm ra hình giống nhau giữa hai thẻ. Cả bàn cùng phá hết chồng thẻ trước khi hết giờ.")
  prerequisite: qsTr("Đọc được tiếng Việt.")
  manual: qsTr("Học hình: một mình, nhớ mặt và tên 57 hình của làng qua năm mức.") + "<br><br>" +
          qsTr("Luật làng: 2 đến 6 người quanh một máy. Máy chia bài, lật thẻ và bấm giờ; các con nhìn chung hai thẻ rồi REO TO tên hình giống nhau. Ai gọi được thì bấm vào ô tên mình, rồi bấm vào hình đó.") + "<br><br>" +
          qsTr("Cả bàn thắng cùng nhau, không ai thắng một mình. Bạn làm Hoa tiêu không được ghi lượt, nhưng bấm phím cách để nháy gợi ý cho cả bàn.")
  credit: ""
  section: "langmaker discovery"
  createdInVersion: 0
}
