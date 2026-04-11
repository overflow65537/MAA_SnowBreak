"""
MAA_SnowBreak
MAA_SnowBreak 通知
作者:overflow65537
"""

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import OCRResult
import json
import datetime
import unicodedata
import smtplib
import ssl
import time
import subprocess
from email.mime.text import MIMEText
from email.header import Header

try:
    import winsound
except ImportError:
    winsound = None


class Notice(CustomAction):
    def _parse_param(self, raw):
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str) and raw.strip():
            return json.loads(raw)
        return {}

    def normalize_number(self, text: str) -> str:
        """Normalize OCR number text into plain ASCII digits."""
        if not isinstance(text, str):
            return "0"
        normalized = unicodedata.normalize("NFKC", text).strip()
        for ch in [",", " ", "\u00A0", "_", "'"]:
            normalized = normalized.replace(ch, "")
        return normalized

    def _send_alarm(self, alarm_param: dict):
        enabled = alarm_param.get("enabled", True)
        if not enabled:
            return
        times = int(alarm_param.get("times", 3))
        frequency = int(alarm_param.get("frequency", 1200))
        duration_ms = int(alarm_param.get("duration_ms", 300))
        interval_ms = int(alarm_param.get("interval_ms", 400))

        if winsound is not None:
            for idx in range(max(1, times)):
                try:
                    winsound.Beep(max(37, frequency), max(50, duration_ms))
                except RuntimeError:
                    winsound.MessageBeep()
                if idx < times - 1:
                    time.sleep(max(0, interval_ms) / 1000.0)
            return

        for idx in range(max(1, times)):
            print("\a", end="", flush=True)
            if idx < times - 1:
                time.sleep(max(0, interval_ms) / 1000.0)

    def _send_email(self, email_param: dict, content: str):
        enabled = email_param.get("enabled", True)
        if not enabled:
            return

        smtp_host = email_param.get("smtp_host")
        smtp_port = int(email_param.get("smtp_port", 465))
        username = email_param.get("username")
        password = email_param.get("password")
        from_addr = email_param.get("from", username)
        to_addr = email_param.get("to", [])
        if isinstance(to_addr, str):
            raw = to_addr.replace(";", ",")
            to_addr = [x.strip() for x in raw.split(",") if x.strip()]

        if not (smtp_host and username and password and from_addr and to_addr):
            raise ValueError("email config missing required fields")

        subject = email_param.get("subject", "MAA_SnowBreak 通知")
        use_ssl = email_param.get("use_ssl", True)
        use_starttls = email_param.get("use_starttls", False)

        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addr)

        if use_ssl:
            context_ssl = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                smtp_host, smtp_port, context=context_ssl, timeout=15
            ) as server:
                server.login(username, password)
                server.sendmail(from_addr, to_addr, msg.as_string())
            return

        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.ehlo()
            if use_starttls:
                context_tls = ssl.create_default_context()
                server.starttls(context=context_tls)
                server.ehlo()
            server.login(username, password)
            server.sendmail(from_addr, to_addr, msg.as_string())

    def _show_powershell_popup(self, popup_param: dict, title: str, content: str):
        enabled = popup_param.get("enabled", True)
        if not enabled:
            return

        timeout_sec = int(popup_param.get("timeout_sec", 15))
        icon = int(popup_param.get("icon", 48))  # 48: warning icon
        popup_title = popup_param.get("title", title or "MAA_SnowBreak 通知")
        popup_message = popup_param.get("message", content)

        # Escape single quote for PowerShell single-quoted string.
        ps_title = str(popup_title).replace("'", "''")
        ps_message = str(popup_message).replace("'", "''")
        script = (
            "$wshell = New-Object -ComObject WScript.Shell; "
            f"$null = $wshell.Popup('{ps_message}', {max(1, timeout_sec)}, '{ps_title}', {icon})"
        )

        kwargs = {"check": False, "timeout": max(3, timeout_sec + 5)}
        create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", None)
        if create_no_window is not None:
            kwargs["creationflags"] = create_no_window

        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
            **kwargs,
        )

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        param: dict = self._parse_param(argv.custom_action_param)
        action = param.get("action")
        if action == "set_Currency":
            image = context.tasker.controller.post_screencap().wait().get()
            Currency_reco = context.run_recognition("识别数据金", image)
            if (
                Currency_reco
                and Currency_reco.hit
                and isinstance(Currency_reco.best_result, OCRResult)
            ):
                Currency = Currency_reco.best_result.text

            else:
                Currency = "0"

            context.tasker.resource.override_pipeline(
                {"资源变量": {"focus": {"start_Currency": Currency}}}
            )
        elif action == "show_Currency":
            image = context.tasker.controller.post_screencap().wait().get()
            end_Currency_reco = context.run_recognition("识别数据金", image)

            if (
                end_Currency_reco
                and end_Currency_reco.hit
                and isinstance(end_Currency_reco.best_result, OCRResult)
            ):
                end_Currency = end_Currency_reco.best_result.text
            else:
                end_Currency = "0"

            energy_reco = context.run_recognition("识别体力", image)

            if (
                energy_reco
                and energy_reco.hit
                and isinstance(energy_reco.best_result, OCRResult)
            ):
                energy = energy_reco.best_result.text
            else:
                energy = "0"

            resource = context.get_node_object("资源变量")
            if resource is None:
                return CustomAction.RunResult(success=True)
            start_Currency = resource.focus.get("start_Currency")

            # 收益
            start_currency_norm = self.normalize_number(start_Currency)
            end_currency_norm = self.normalize_number(end_Currency)
            energy_norm = self.normalize_number(energy)
            if (
                start_currency_norm.isdigit()
                and end_currency_norm.isdigit()
                and energy_norm.isdigit()
            ):
                profit = int(end_currency_norm) - int(start_currency_norm)
                next_energy = 240 - int(energy_norm) * 6 * 60

                now_time = datetime.datetime.now()
                next_time = now_time + datetime.timedelta(seconds=next_energy)
                self.custom_notify(context, f"初始数据金: {start_currency_norm}")
                self.custom_notify(context, f"当前数据金: {end_currency_norm}")
                self.custom_notify(context, f"收益: {profit}")
                self.custom_notify(
                    context,
                    f"下次体力恢复时间:{next_time.strftime('%Y-%m-%d %H:%M:%S')}",
                )
        elif action == "notify":
            message = param.get("message", "MAA_SnowBreak 通知")
            self.custom_notify(context, message)
        elif action == "multi_notify":
            message = param.get("message", "MAA_SnowBreak 通知")
            title = param.get("title", "MAA_SnowBreak")
            full_message = f"[{title}] {message}" if title else message
            focus_event = param.get("focus_event", "Node.Action.Succeeded")
            focus_display = param.get(
                "focus_display", ["log", "toast", "notification", "dialog"]
            )
            if isinstance(focus_display, str):
                focus_display = [focus_display]
            self.custom_notify(
                context, full_message, event=focus_event, display=focus_display
            )

            alarm_param = param.get("alarm", {})
            if isinstance(alarm_param, dict):
                try:
                    self._send_alarm(alarm_param)
                except Exception as exc:
                    self.custom_notify(context, f"[Notice] 闹钟失败: {exc}")

            email_param = param.get("email", {})
            if isinstance(email_param, dict) and email_param:
                try:
                    self._send_email(email_param, full_message)
                except Exception as exc:
                    self.custom_notify(context, f"[Notice] 邮件失败: {exc}")

            popup_param = param.get("popup", {})
            if isinstance(popup_param, dict):
                try:
                    self._show_powershell_popup(popup_param, title, full_message)
                except Exception as exc:
                    self.custom_notify(context, f"[Notice] 弹窗失败: {exc}")
        elif action:
            self.custom_notify(context, f"[Notice] 未知 action: {action}")

        return CustomAction.RunResult(success=True)

    def custom_notify(
        self,
        context: Context,
        msg: str,
        event: str = "Node.Recognition.Succeeded",
        display=None,
    ):
        """自定义通知"""
        event_payload = msg
        if display is not None:
            event_payload = {"content": msg, "display": display}
        context.override_pipeline(
            {"custom通知": {"focus": {event: event_payload}}}
        )
        context.run_task("custom通知")
