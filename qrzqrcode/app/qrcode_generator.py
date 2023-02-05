import io
from PIL import Image
import qrcode
import requests


_LOGO_URI = 'https://www.qrz.com/apple-touch-icon-114x114.png'
_PROFILE_URL_FORMAT = 'https://www.qrz.com/db/{callsign}'
_LOGO_TO_QRCODE_SIZE_RATIO = 0.25


def _download_logo_image():
    resp = requests.get(_LOGO_URI)
    resp.raise_for_status()

    logo_octets = io.BytesIO(resp.content)

    return Image.open(logo_octets)


_LOGO = _download_logo_image()


def _generate_profile_url(callsign):
    return _PROFILE_URL_FORMAT.format(callsign=callsign)


def _add_logo(qr_img, logo):
    qr_width, qr_height = qr_img.size

    # assume logo width == logo height
    desired_logo_size = int(qr_width * _LOGO_TO_QRCODE_SIZE_RATIO)

    logo = logo.resize((desired_logo_size, desired_logo_size), Image.ANTIALIAS)

    position = (
        (qr_width - desired_logo_size) // 2,
        (qr_height - desired_logo_size) // 2
    )

    qr_img.paste(logo, position)

    return qr_img


def generate_qrcode_image(callsign: str):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    profile_url = _generate_profile_url(callsign)
    qr.add_data(profile_url)
    qr.make()

    qr_img = qr.make_image(fill_color='black').convert('RGBA')

    qr_img = _add_logo(qr_img, _LOGO)

    return qr_img
