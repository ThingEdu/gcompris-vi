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
  goal: qsTr("Nhìn nhanh, gọi to, tìm ra hình giống nhau giữa hai thẻ. Mỗi ván chơi đúng 12 lượt, không tính giờ để thắng thua.")
  prerequisite: qsTr("Đọc được tiếng Việt.")
  manual: qsTr("Học hình: một mình, nhớ mặt và tên 57 hình của làng qua năm mức.") + "<br><br>" +
          qsTr("Luật làng: 2 đến 6 người quanh một máy. Máy chia bài; các con nhìn chung hai thẻ rồi REO TO tên hình giống nhau. Ai gọi được thì bấm vào ô tên mình, rồi bấm vào hình đó — cả bàn đổi thẻ mới ngay. Ván chơi đúng 12 lượt. Trong ván không ai thấy điểm của ai; chỉ tới cuối ván mới nhắc nhẹ nếu có bạn gọi được nhiều hơn hẳn.") + "<br><br>" +
          qsTr("Luật ăn thua: cũng 2 đến 6 người và 12 lượt, nhưng mỗi lượt máy che thẻ đếm 3-2-1 trước khi cho nhìn; gọi đúng thì ghi điểm ngay, điểm hiện công khai dưới tên suốt ván, cả thẻ chung lẫn thẻ riêng đều đổi mới.") + "<br><br>" +
          qsTr("Cả bàn thắng cùng nhau, không ai thắng một mình. Bạn làm Hoa tiêu không được ghi lượt, nhưng bấm phím cách để nháy gợi ý cho cả bàn.")
  credit: qsTr("Bộ 57 hình Làng Maker: © ThingEdu, giấy phép CC BY-SA 4.0. Linh vật Tux là bản vẽ lại; linh vật Linux gốc của Larry Ewing.")
  section: "langmaker discovery"
  createdInVersion: 0
}
