"""Write the frame of the rebuilt workbook: the READ ME page, the column directory and one empty sheet per trade day.

No market data is written. The trade-day sheets hold their header rows only; they are filled by the ROOT build.
Usage: make_workbook_frame.py <README wording .md> <LAYER_REGISTRY.json> <out.xlsx>
"""
import json, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

TRADE_DAYS = ['Mon 2023-10-02', 'Tue 2023-10-03', 'Tue 2023-10-17', 'Wed 2023-10-18']
FOUNDATION = 'ROOT part 1 (foundation)'
EMPTY = 'empty until the ROOT build fills it'

# (section, column, what it is in plain words, where it comes from)
COLUMNS = [
 ('A. The native tape', 'exchange_time_ns', 'When the exchange says it happened (UTC nanoseconds).', 'tape'),
 ('A. The native tape', 'received_time_ns', 'When the message reached the data vendor at the exchange: the first moment it could be known.', 'tape'),
 ('A. The native tape', 'action', 'What the message is: add, cancel, modify, trade, fill, clear or none.', 'tape'),
 ('A. The native tape', 'side', 'Bid, ask or none. On a trade row this is the trade side exactly as the tape gives it.', 'tape'),
 ('A. The native tape', 'price', 'The price on the message. On a trade row, the trade price.', 'tape'),
 ('A. The native tape', 'size', 'The size on the message. On a trade row, the trade size.', 'tape'),
 ('A. The native tape', 'order_number', 'The exchange order number. A label only.', 'tape'),
 ('A. The native tape', 'flags', 'The exchange flags on the message, as sent.', 'tape'),
 ('A. The native tape', 'ends_exchange_event', 'Yes when this tick carries the exchange end-of-event flag.', 'tape'),
 ('A. The native tape', 'sequence_number', 'The exchange sequence number. Shared with other contracts on the channel, so jumps forward are normal.', 'tape'),
 ('A. The native tape', 'channel', 'The exchange channel number.', 'tape'),
 ('A. The native tape', 'publisher', 'The data vendor publisher number.', 'tape'),
 ('A. The native tape', 'contract_number', 'The exchange number of the contract.', 'tape'),
 ('A. The native tape', 'send_delay_ns', 'The delay the tape reports between the exchange sending and the vendor receiving.', 'tape'),
 ('B. Our labels', 'row_label', 'One of: a trade day; the 5 pm to 6 pm stretch; the Sunday start-up. Decided by exchange time.', 'label'),
 ('B. Our labels', 'trade_day', 'The trade day (6 pm Eastern the evening before to 5 pm Eastern). Empty on stretch and start-up rows.', 'label'),
 ('B. Our labels', 'position_on_tape', 'The place of this tick on the tape for the week. A label only.', 'label'),
 ('B. Our labels', 'raw_file', 'The raw file this row came from.', 'label'),
 ('B. Our labels', 'raw_file_fingerprint', 'The fingerprint (SHA256) of that raw file.', 'label'),
 ('B. Our labels', 'contract', 'The contract symbol, read from the tape.', 'label'),
 ('B. Our labels', 'in_settlement_window', 'Yes on rows inside the 2:28 to 2:30 pm Eastern settlement window.', 'label'),
 ('B. Our labels', 'exchange_event', 'Which exchange event this tick belongs to: the position of the event first tick.', 'label'),
 ('C. What this tick did', 'order_size_before', 'The touched order size just before this tick.', 'book'),
 ('C. What this tick did', 'order_size_after', 'The touched order size just after this tick.', 'book'),
 ('C. What this tick did', 'what_happened', 'Joined, stayed, shrank, lost its place in line, left by cancel, or left by fill.', 'book'),
 ('C. What this tick did', 'orders_ahead_before', 'How many orders were ahead of it in line just before.', 'book'),
 ('C. What this tick did', 'size_ahead_before', 'How much size was ahead of it in line just before.', 'book'),
 ('C. What this tick did', 'life_step', 'Which step of this order life this is so far.', 'book'),
 ('C. What this tick did', 'first_entered_position', 'The tick where this order first entered.', 'book'),
 ('C. What this tick did', 'previous_step_position', 'The tick of this order previous step.', 'book'),
 ('C. What this tick did', 'first_entered_exchange_time_ns', 'When it first entered, exchange time.', 'book'),
 ('C. What this tick did', 'first_entered_received_time_ns', 'When it first entered, received time.', 'book'),
 ('C. What this tick did', 'took_place_exchange_time_ns', 'When it last took its place in line, exchange time.', 'book'),
 ('C. What this tick did', 'took_place_received_time_ns', 'When it last took its place in line, received time.', 'book'),
 ('C. What this tick did', 'rested_exchange_ns', 'How long it has held its place, on exchange time.', 'book'),
 ('C. What this tick did', 'rested_received_ns', 'How long it has held its place, on received time.', 'book'),
 ('C. What this tick did', 'rested_is_at_least', 'Yes when the order was carried over the weekend, so its true age is not on the tape.', 'book'),
 ('C. What this tick did', 'levels_from_best', 'How many price levels from the best price the action happened at.', 'book'),
 ('C. What this tick did', 'irregular', 'Anything irregular on this tick, in words. Empty when nothing is.', 'book'),
 ('D. The book at this tick', 'best_bid', 'Best bid price.', 'book'),
 ('D. The book at this tick', 'best_ask', 'Best ask price.', 'book'),
 ('D. The book at this tick', 'gap', 'Best ask minus best bid.', 'book'),
 ('D. The book at this tick', 'bid_total_size', 'Total size resting on the bid side, whole book.', 'book'),
 ('D. The book at this tick', 'bid_orders', 'Number of orders on the bid side, whole book.', 'book'),
 ('D. The book at this tick', 'bid_levels', 'Number of price levels on the bid side, whole book.', 'book'),
 ('D. The book at this tick', 'ask_total_size', 'Total size resting on the ask side, whole book.', 'book'),
 ('D. The book at this tick', 'ask_orders', 'Number of orders on the ask side, whole book.', 'book'),
 ('D. The book at this tick', 'ask_levels', 'Number of price levels on the ask side, whole book.', 'book'),
]
for name, word in (('best_bid', 'best bid'), ('best_ask', 'best ask')):
    COLUMNS += [
     ('D. The book at this tick', f'{name}_size', f'Size at the {word}.', 'book'),
     ('D. The book at this tick', f'{name}_orders', f'Number of orders at the {word}.', 'book'),
     ('D. The book at this tick', f'{name}_front_size', f'Size of the order at the front of the line at the {word}.', 'book'),
     ('D. The book at this tick', f'{name}_front_first_entered_exchange_time_ns', 'When that front order first entered, exchange time.', 'book'),
     ('D. The book at this tick', f'{name}_front_first_entered_received_time_ns', 'When that front order first entered, received time.', 'book'),
     ('D. The book at this tick', f'{name}_front_took_place_exchange_time_ns', 'When that front order last took its place, exchange time.', 'book'),
     ('D. The book at this tick', f'{name}_front_took_place_received_time_ns', 'When that front order last took its place, received time.', 'book'),
     ('D. The book at this tick', f'{name}_front_is_at_least', 'Yes when that front order was carried over the weekend.', 'book'),
    ]
COLUMNS += [
 ('D. The book at this tick', 'touched_price', 'The price this tick acted on.', 'book'),
 ('D. The book at this tick', 'touched_line', 'The full line at that price after this tick: every order in order, with its size and times.', 'book'),
 ('D. The book at this tick', 'touched_line_size_before', 'Total size in that line just before.', 'book'),
 ('D. The book at this tick', 'touched_line_size_after', 'Total size in that line just after.', 'book'),
 ('D. The book at this tick', 'touched_line_orders_before', 'Number of orders in that line just before.', 'book'),
 ('D. The book at this tick', 'touched_line_orders_after', 'Number of orders in that line just after.', 'book'),
 ('E. Change-of-state marks', 'best_bid_moved_from', 'The old best bid, when this tick moved it.', 'book'),
 ('E. Change-of-state marks', 'best_bid_moved_to', 'The new best bid, when this tick moved it.', 'book'),
 ('E. Change-of-state marks', 'best_ask_moved_from', 'The old best ask, when this tick moved it.', 'book'),
 ('E. Change-of-state marks', 'best_ask_moved_to', 'The new best ask, when this tick moved it.', 'book'),
 ('E. Change-of-state marks', 'level_appeared', 'Yes when this tick made a new price level appear.', 'book'),
 ('E. Change-of-state marks', 'level_emptied', 'Yes when this tick emptied a price level.', 'book'),
 ('E. Change-of-state marks', 'front_of_line_changed', 'Yes when this tick changed which order is at the front of a line.', 'book'),
]


def main(readme_md, registry_json, out):
    registry = {r['column'].split(' | ')[0]: r for r in json.load(open(registry_json))}
    outside = [(f'G. The 13 outside data points', k, registry[k]['description'], 'outside') for k in sorted(registry) if k.startswith('X')]
    part2 = [k for k in sorted(registry) if (k.startswith('L') and (49 <= int(k[1:]) <= 51 or 59 <= int(k[1:]) <= 71 or int(k[1:]) in (75, 76))) or k.startswith('S')]
    later = [('H. ROOT part 2 (calculations, not designed yet)', k, registry[k]['description'], 'part 2') for k in part2]
    step1 = [('I. Step 1 and the 2021 work (handled separately)', k, registry[k]['description'], 'step 1')
             for k in sorted(registry) if k.startswith('L') and (54 <= int(k[1:]) <= 58 or int(k[1:]) == 80 or 83 <= int(k[1:]) <= 89)]
    frankie = [('J. Frankie outputs (blank)', k, registry[k]['description'], 'frankie')
               for k in sorted(registry) if k.startswith('L') and (77 <= int(k[1:]) <= 79 or 90 <= int(k[1:]) <= 99)]
    all_cols = COLUMNS + outside + later + step1 + frankie
    names = [c[1] for c in all_cols]
    assert len(names) == len(set(names)), 'a column name is repeated'

    wb = Workbook()
    bold = Font(bold=True)
    ws = wb.active
    ws.title = 'READ ME FIRST'
    ws.column_dimensions['A'].width = 150
    text = open(readme_md, encoding='utf-8').read().split('\n---\n', 1)[1]
    row = 1
    for line in text.split('\n'):
        line = line.rstrip()
        if not line.strip():
            row += 1
            continue
        plain = re.sub(r'\*\*(.+?)\*\*', r'\1', line).replace('`', '')
        cell = ws.cell(row=row, column=1, value=plain.lstrip('# ') if plain.startswith('#') else plain)
        if line.startswith('#'):
            cell.font = bold
        cell.alignment = Alignment(wrap_text=True, vertical='top')
        row += 1

    wc = wb.create_sheet('COLUMNS')
    for i, h in enumerate(['Section', 'Column', 'What it is', 'Comes from', 'Shown to Frankie', 'State'], 1):
        wc.cell(row=1, column=i, value=h).font = bold
    for r, (section, col, what, src) in enumerate(all_cols, 2):
        state = EMPTY if src in ('tape', 'label', 'book', 'outside') else {
            'part 2': 'empty: to be worked out in ROOT part 2', 'step 1': 'empty: handled separately',
            'frankie': 'blank until a Frankie run'}[src]
        for i, v in enumerate([section, col, what, src, 'shown', state], 1):
            wc.cell(row=r, column=i, value=v)
    for letter, width in zip('ABCDEF', (46, 48, 110, 12, 18, 44)):
        wc.column_dimensions[letter].width = width
    wc.freeze_panes = 'A2'

    for day in TRADE_DAYS:
        wd = wb.create_sheet('TD ' + day)
        for i, (section, col, _what, _src) in enumerate(all_cols, 1):
            wd.cell(row=1, column=i, value=section)
            wd.cell(row=2, column=i, value=col).font = bold
        wd.cell(row=3, column=1, value='No rows yet. This sheet is filled by the ROOT build, one row per tick. Nothing here is missing data.')
        wd.freeze_panes = 'A3'
    wb.save(out)
    print(f'{out}: {len(wb.sheetnames)} sheets, {len(all_cols)} columns '
          f'({len(COLUMNS)} foundation, {len(outside)} outside, {len(later)} part 2, {len(step1)} step 1, {len(frankie)} Frankie)')


if __name__ == '__main__':
    main(*sys.argv[1:4])
