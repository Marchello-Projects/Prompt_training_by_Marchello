import os
import sqlite3
from datetime import datetime
import pytz
import xlsxwriter

from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import FSInputFile

router = Router()
ITEMS_PER_PAGE = 10
kyiv_tz = pytz.timezone('Europe/Kyiv')


def get_history_page(page: int):
    offset = page * ITEMS_PER_PAGE
    with sqlite3.connect('app/database/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT mode, prompt, created_at FROM History ORDER BY created_at DESC LIMIT ? OFFSET ?',
            (ITEMS_PER_PAGE, offset)
        )
        rows = cursor.fetchall()
    return rows


def build_history_keyboard(page: int, has_prev: bool, has_next: bool):
    row = []
    if has_prev:
        row.append(InlineKeyboardButton(text='⬅️ Prev', callback_data=f'history_page:{page-1}'))
    if page > 0:
        row.append(InlineKeyboardButton(text='⬆️ Top', callback_data='history_page:0'))
    if has_next:
        row.append(InlineKeyboardButton(text='➡️ Next', callback_data=f'history_page:{page+1}'))

    export = InlineKeyboardButton(text='📥 Export to Excel', callback_data='export_excel')
    clear = InlineKeyboardButton(text='🗑️ Clear History', callback_data='clear_history')

    return InlineKeyboardMarkup(inline_keyboard=[row, [export, clear]])


def export_history_to_excel():
    filepath = 'history_export.xlsx'
    with sqlite3.connect('app/database/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT mode, prompt, created_at FROM History ORDER BY created_at DESC')
        rows = cursor.fetchall()
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()
    headers = ['Mode', 'Prompt', 'Created At']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    for row_idx, row in enumerate(rows, start=1):
        mode, prompt, created_at = row
        created_at = datetime.fromisoformat(created_at).astimezone(kyiv_tz).strftime('%Y-%m-%d %H:%M')
        worksheet.write(row_idx, 0, mode)
        worksheet.write(row_idx, 1, prompt)
        worksheet.write(row_idx, 2, created_at)
    workbook.close()
    return filepath


@router.message(F.text == '🕒 History')
async def show_history(message: Message):
    page = 0
    rows = get_history_page(page)
    if not rows:
        await message.answer('History is empty')
        return
    text = f'Page {page+1}:\n\n'
    for mode, prompt, created_at in rows:
        created_at = datetime.fromisoformat(created_at).astimezone(kyiv_tz).strftime('%Y-%m-%d %H:%M')
        text += f'📅 {created_at}\n🎯 Type: {mode}\n💬 Prompt: {prompt}\n\n'
    with sqlite3.connect('app/database/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM History')
        total = cursor.fetchone()[0]
    has_next = (page + 1) * ITEMS_PER_PAGE < total
    keyboard = build_history_keyboard(page, has_prev=False, has_next=has_next)
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data and c.data.startswith('history_page:'))
async def history_page_callback(callback: CallbackQuery):
    page = int(callback.data.split(':')[1])
    rows = get_history_page(page)
    if not rows:
        await callback.answer('No more records.')
        return
    text = f'Page {page+1}:\n\n'
    for mode, prompt, created_at in rows:
        created_at = datetime.fromisoformat(created_at).astimezone(kyiv_tz).strftime('%Y-%m-%d %H:%M')
        text += f'📅 {created_at}\n🎯 Type: {mode}\n💬 Prompt: {prompt}\n\n'
    with sqlite3.connect('app/database/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM History')
        total = cursor.fetchone()[0]
    has_prev = page > 0
    has_next = (page + 1) * ITEMS_PER_PAGE < total
    keyboard = build_history_keyboard(page, has_prev=has_prev, has_next=has_next)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == 'export_excel')
async def handle_export_excel(callback: CallbackQuery):
    path = export_history_to_excel()
    if os.path.exists(path):
        file = FSInputFile(path)
        await callback.message.answer_document(file, caption='📄 Here is your exported history.')
    else:
        await callback.message.answer('⚠️ Failed to export.')
    await callback.answer()


@router.callback_query(F.data == 'clear_history')
async def handle_clear_history(callback: CallbackQuery):
    with sqlite3.connect('app/database/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM History')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="History"')
        conn.commit()
    await callback.message.edit_text('🗑️ History cleared.')
    await callback.answer('Cleared!')